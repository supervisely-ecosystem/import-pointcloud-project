import functools
import os
import tarfile
import zipfile
from os.path import basename, dirname, normpath
from typing import Callable

import download_progress
import globals as g
import supervisely as sly
from supervisely.pointcloud_annotation.constants import NAME, TAGS


def update_progress(count, api: sly.Api, task_id: int, progress: sly.Progress) -> None:
    count = min(count, progress.total - progress.current)
    progress.iters_done(count)
    if progress.need_report():
        progress.report_progress()


def get_progress_cb(
    api: sly.Api,
    task_id: int,
    message: str,
    total: int,
    is_size: bool = False,
    func: Callable = update_progress,
) -> functools.partial:
    progress = sly.Progress(message, total, is_size=is_size)
    progress_cb = functools.partial(func, api=api, task_id=task_id, progress=progress)
    progress_cb(0)
    return progress_cb


def get_project_name_from_input_path(input_path: str) -> str:
    """Returns project name from target sly folder name."""
    full_path_dir = os.path.dirname(input_path)
    return os.path.basename(full_path_dir)


def search_projects(dir_path):
    files = os.listdir(dir_path)
    meta_exists = "meta.json" in files
    datasets = [f for f in files if sly.fs.dir_exists(os.path.join(dir_path, f))]
    datasets_exists = len(datasets) > 0
    return meta_exists and datasets_exists


def search_pcd_dir(dir_path):
    listdir = os.listdir(dir_path)
    is_pcd_dir = any(
        sly.fs.get_file_ext(f) in sly.pointcloud.ALLOWED_POINTCLOUD_EXTENSIONS for f in listdir
    )
    return is_pcd_dir


def is_archive_path(path):
    """Checks if remote path is archive."""
    return sly.fs.get_file_ext(path) in [".zip", ".tar"] or path.endswith(".tar.gz")


def check_input_path(api, input_dir: str, input_file: str) -> str:
    """Checks the input path."""

    if input_dir:
        listdir = api.file.listdir(g.TEAM_ID, input_dir)
        archives_cnt = len([file for file in listdir if is_archive_path(file)])
        if archives_cnt > 1:
            raise Exception("Multiple archives are not supported.")
        if len(listdir) == 1 and archives_cnt == 1:
            sly.logger.info(
                "Folder mode is selected, but archive file is uploaded. Switching to file mode."
            )
            input_dir, input_file = None, listdir[0]

    if input_file:
        file_ext = sly.fs.get_file_ext(input_file)
        if not is_archive_path(input_file):
            sly.logger.info("File mode is selected, but uploaded file is not archive.")
            if basename(normpath(input_file)) in ["meta.json", "key_id_map.json"]:
                input_dir, input_file = dirname(input_file), None
            if input_file and (sly.image.has_valid_ext(input_file) or file_ext == ".json"):
                if dirname(dirname(normpath(input_file))) == "related_images":
                    possible_dataset_dir = dirname(dirname(dirname(normpath(input_file))))
                    dataset_listdir = api.file.listdir(g.TEAM_ID, possible_dataset_dir)
                    if all(
                        basename(normpath(x)) in ["pointcloud", "ann", "related_images"]
                        for x in dataset_listdir
                        if api.file.dir_exists(g.TEAM_ID, x)
                    ):
                        possible_project_dir = dirname(normpath(possible_dataset_dir))
                        project_listdir = api.file.listdir(g.TEAM_ID, possible_project_dir)
                        if any(basename(normpath(x)) == "meta.json" for x in project_listdir):
                            sly.logger.info(f"Found meta.json in {possible_project_dir}.")
                            input_dir, input_file = possible_project_dir, None
            if input_file and (sly.pointcloud.has_valid_ext(input_file) or file_ext == ".json"):
                possible_dataset_dir = dirname(dirname(normpath(input_file)))
                dataset_listdir = api.file.listdir(g.TEAM_ID, possible_dataset_dir)
                if all(
                    basename(normpath(x)) in ["pointcloud", "ann", "related_images"]
                    for x in dataset_listdir
                    if api.file.dir_exists(g.TEAM_ID, x)
                ):
                    possible_project_dir = dirname(normpath(possible_dataset_dir))
                    project_listdir = api.file.listdir(g.TEAM_ID, possible_project_dir)
                    if any(basename(normpath(x)) == "meta.json" for x in project_listdir):
                        sly.logger.info(f"Found meta.json in {possible_project_dir}.")
                        input_dir, input_file = possible_project_dir, None
            if input_file and sly.pointcloud.has_valid_ext(input_file):
                input_dir, input_file = dirname(normpath(input_file)), None

    return input_dir, input_file


def download_input_files(api, task_id, input_dir, input_file):
    if input_dir:
        if g.IS_ON_AGENT:
            agent_id, cur_files_path = api.file.parse_agent_id_and_path(input_dir)
        else:
            cur_files_path = input_dir

        sizeb = api.file.get_directory_size(g.TEAM_ID, input_dir)
        extract_dir = os.path.join(g.storage_dir, cur_files_path.strip("/"))
        # project_name = Path(cur_files_path).name
        progress_cb = download_progress.get_progress_cb(
            api, task_id, f"Downloading {g.INPUT_DIR.strip('/')}", sizeb, is_size=True
        )
        api.file.download_directory(g.TEAM_ID, input_dir, extract_dir, progress_cb)
    else:
        if g.IS_ON_AGENT:
            agent_id, cur_files_path = api.file.parse_agent_id_and_path(input_file)
        else:
            cur_files_path = input_file

        sizeb = api.file.get_info_by_path(g.TEAM_ID, input_file).sizeb
        archive_path = os.path.join(g.storage_dir, sly.fs.get_file_name_with_ext(cur_files_path))
        extract_dir = os.path.join(g.storage_dir, sly.fs.get_file_name(cur_files_path))
        # project_name = sly.fs.get_file_name(input_file)
        progress_cb = download_progress.get_progress_cb(
            api, task_id, f"Downloading {g.INPUT_FILE.lstrip('/')}", sizeb, is_size=True
        )
        api.file.download(g.TEAM_ID, input_file, archive_path, None, progress_cb)

        if sly.fs.is_archive(archive_path):
            sly.fs.unpack_archive(archive_path, extract_dir)
            sly.fs.silent_remove(archive_path)
        else:
            raise Exception(
                f"Incorrect file format '{archive_path}'. Please use .tar or .zip files."
            )
    return extract_dir


def get_project_dirs(input_dir):
    project_dirs = [project_dir for project_dir in sly.fs.dirs_filter(input_dir, search_projects)]

    only_pcd_dirs = []
    if len(project_dirs) == 0:
        only_pcd_dirs = [pcd_dir for pcd_dir in sly.fs.dirs_filter(input_dir, search_pcd_dir)]
    return project_dirs, only_pcd_dirs


def upload_only_pcds(api: sly.Api, task_id, project_name, only_pcd_dirs):
    project = None
    pcd_cnt = 0
    for pcd_dir in only_pcd_dirs:
        if not sly.fs.dir_exists(pcd_dir):
            continue
        pcd_paths = sly.fs.list_files(
            pcd_dir,
            valid_extensions=sly.pointcloud.ALLOWED_POINTCLOUD_EXTENSIONS,
            ignore_valid_extensions_case=True,
        )
        if len(pcd_paths) == 0:
            continue
        if project is None:
            project = api.project.create(
                g.WORKSPACE_ID,
                project_name,
                type=sly.ProjectType.POINT_CLOUDS,
                change_name_if_conflict=True,
            )
        total_size = sum([sly.fs.get_file_size(path) for path in pcd_paths])
        dataset = api.dataset.create(project.id, "ds0", change_name_if_conflict=True)
        progress_project_cb = get_progress_cb(
            api,
            task_id,
            f"Uploading pointclouds from directory '{pcd_dir}' to dataset '{dataset.name}'",
            total_size,
        )
        pcd_names = [basename(path) for path in pcd_paths if sly.pointcloud.has_valid_ext(path)]
        pointclouds = api.pointcloud.upload_paths(
            dataset.id, pcd_names, pcd_paths, progress_project_cb
        )
        pcd_cnt += len(pointclouds)
    if pcd_cnt > 1:
        sly.logger.info(f"{pcd_cnt} pointclouds were uploaded to project '{project.name}'.")
    elif pcd_cnt == 1:
        sly.logger.info(f"{pcd_cnt} pointcloud was uploaded to project '{project.name}'.")

    if project is None:
        return pcd_cnt, None
    return pcd_cnt, project.id


def check_project_structure(project_dir):
    scandir = os.scandir(project_dir)
    meta_path = os.path.join(project_dir, "meta.json")
    meta_json = sly.json.load_json_file(meta_path)
    project_meta = sly.ProjectMeta.from_json(meta_json)
    for path in scandir:
        if path.is_dir():
            pcd_dir = os.path.join(path.path, "pointcloud")
            ann_dir = os.path.join(path.path, "ann")
            pcd_files = os.listdir(pcd_dir)
            if not sly.fs.dir_exists(pcd_dir):
                raise Exception(f"Pointcloud directory not found in {path.path}.")
            if not sly.fs.dir_exists(ann_dir):
                raise Exception(f"Annotation directory not found in {path.path}.")
            for ann in os.scandir(ann_dir):
                if ann.is_file():
                    try:
                        ann_json = sly.json.load_json_file(ann.path)
                        sly.PointcloudAnnotation.from_json(ann_json, project_meta)
                    except Exception as e:
                        new_msg = f"{ann.name}: Annotation file is not valid: {e}."
                        tag_names = [tagmeta.name for tagmeta in project_meta.tag_metas]
                        if "TagMeta is None" in str(e):
                            for tag in ann_json[TAGS]:
                                if NAME not in tag:
                                    new_msg = f"{ann.name}: Name field not found for one of the tags in uploaded annotation. Skippping file..."
                                elif tag[NAME] not in tag_names:
                                    new_msg = f"{ann.name}: Tag '{tag[NAME]}' not found in given project meta. Skippping file..."
                        sly.logger.warn(new_msg)
                        sly.fs.silent_remove(ann.path)
            if len(pcd_files) != len(os.listdir(ann_dir)):
                for pcd in pcd_files:
                    if f"{pcd}.json" not in os.listdir(ann_dir):
                        ann_path = os.path.join(ann_dir, f"{pcd}.json")
                        sly.json.dump_json_file(sly.PointcloudAnnotation().to_json(), ann_path)
                    if sly.fs.get_file_size(os.path.join(pcd_dir, pcd)) == 0:
                        sly.logger.warn(f"Pointcloud {pcd} is empty. Skipping...")
                        sly.fs.silent_remove(os.path.join(pcd_dir, pcd))
