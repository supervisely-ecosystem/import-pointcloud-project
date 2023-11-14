import os
import globals as g
import functions as f
import supervisely as sly
from supervisely.project.pointcloud_project import upload_pointcloud_project


@g.my_app.callback("import_pointcloud_project")
@sly.timeit
def import_pointcloud_project(api: sly.Api, task_id, context, state, app_logger):
    if not g.IS_ON_AGENT:
        g.INPUT_DIR, g.INPUT_FILE = f.check_input_path(api, g.INPUT_DIR, g.INPUT_FILE)
    input_dir = f.download_input_files(api, task_id, g.INPUT_DIR, g.INPUT_FILE)

    project_dirs, pcd_dirs = f.get_project_dirs(input_dir)

    uploaded_project_cnt = 0
    uploaded_pcd_cnt = 0

    if len(project_dirs) > 0:
        for project_dir in project_dirs:
            project_id = None
            project_name = os.path.basename(os.path.normpath(project_dir))
            try:
                project_id, project_name = upload_pointcloud_project(
                    project_dir, api, g.WORKSPACE_ID, project_name, log_progress=True
                )
                api.task.set_output_project(task_id, project_id, project_name)
                uploaded_project_cnt += 1
                app_logger.info(
                    f"Project {project_name} (ID:{project_id}) was successfully uploaded."
                )
            except Exception as e:
                try:
                    if project_id is not None:
                        api.project.remove(project_id)
                    app_logger.warn(
                        f"Project {project_dir} was not uploaded. {repr(e)}. \nTry to upload only pointclouds..."
                    )
                    pcd_dirs = [d for d in sly.fs.dirs_filter(project_dir, f.search_pcd_dir)]
                    pcd_cnt, project_id = f.upload_only_pcds(api, task_id, project_name, pcd_dirs)
                    uploaded_pcd_cnt += pcd_cnt
                    if pcd_cnt == 0:
                        app_logger.warn(f"No pointclouds found in {project_dir}.")
                        if project_id is not None:
                            api.project.remove(project_id)
                except Exception as e:
                    app_logger.warn(f"Failed to upload data from {project_dir}. Error: {repr(e)}")
    elif len(pcd_dirs) > 0:
        project_name = os.path.basename(os.path.commonpath(pcd_dirs))
        pcd_cnt, project_id = f.upload_only_pcds(api, task_id, project_name, pcd_dirs)
        uploaded_pcd_cnt += pcd_cnt
        if pcd_cnt == 0:
            app_logger.warn(f"Failed to upload data from {pcd_dirs}. No pointclouds found.")
            if project_id is not None:
                api.project.remove(project_id)

    if uploaded_project_cnt == 0 and uploaded_pcd_cnt == 0:
        msg = "Failed to upload data. Not found any pointclouds or projects in Supervisely format."
        description = "Please, check the input directory, task logs and try again."
        app_logger.error(msg, exc_info=False)
        api.task.set_output_error(task_id, msg, description)

    if g.REMOVE_SOURCE and not g.IS_ON_AGENT:
        if g.INPUT_DIR:
            api.file.remove(team_id=g.TEAM_ID, path=g.INPUT_DIR)
            source_dir_name = g.INPUT_DIR.strip("/")
            app_logger.info(msg=f"Source directory: '{source_dir_name}' was successfully removed.")
        else:
            api.file.remove(team_id=g.TEAM_ID, path=g.INPUT_FILE)
            app_logger.info(msg=f"Source file: '{g.INPUT_FILE}' was successfully removed.")

    g.my_app.stop()


def main():
    sly.logger.info(
        "Script arguments",
        extra={
            "context.teamId": g.TEAM_ID,
            "context.workspaceId": g.WORKSPACE_ID,
            "modal.state.slyFolder": g.INPUT_DIR,
            "modal.state.slyFile": g.INPUT_FILE,
        },
    )

    g.my_app.run(initial_events=[{"command": "import_pointcloud_project"}])


if __name__ == "__main__":
    sly.main_wrapper("main", main)
