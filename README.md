<div align="center" markdown>
<img src="https://github.com/supervisely-ecosystem/import-pointcloud-project/releases/download/v0.0.0/import_ptc_poster.png">

# Import Pointcloud Project

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#Preparation">Preparation</a> •
  <a href="#How-To-Use">How To Use</a> •
  <a href="#Demo-Projects">Demo Projects</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/import-pointcloud-project)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/import-pointcloud-project)
[![views](https://app.supervise.ly/img/badges/views/supervisely-ecosystem/import-pointcloud-project.png)](https://supervise.ly)
[![runs](https://app.supervise.ly/img/badges/runs/supervisely-ecosystem/import-pointcloud-project.png)](https://supervise.ly)

</div>

## Overview

Import project in Supervisely pointcloud format from folder or archive.

Backward compatible with [`Export pointclouds project in Supervisely format`](https://ecosystem.supervise.ly/apps/export-pointclouds-project-in-supervisely-format) app

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/export-pointclouds-project-in-supervisely-format" src="https://user-images.githubusercontent.com/97401023/193619296-df4ea2b2-e26c-42c2-b98a-bbe578c67fdb.png" width="450px" style='padding-bottom: 20px'/>

🏋️ Starting from version `v1.1.2` application supports import from special directory on your local computer. It is made for Enterprise Edition customers who need to upload tens or even hundreds of gigabytes of data without using drag-ang-drop mechanism:

1. Run agent on your computer where data is stored. Watch [how-to video](https://youtu.be/aO7Zc4kTrVg).
2. Copy your data to special folder on your computer that was created by agent. Agent mounts this directory to your Supervisely instance and it becomes accessible in Team Files. Learn more [in documentation](https://docs.supervise.ly/customization/agents/agent-storage). Watch [how-to video](https://youtu.be/63Kc8Xq9H0U).
3. Go to `Team Files` -> `Supervisely Agent` and find your folder there.
4. Right click to open context menu and start app. Now app will upload data directly from your computer to the platform.

# Preparation

Upload your data in Supervisely pointcloud episodes format to Team Files. It is possible to upload folder or archive (`.tar`, `.tar.gz` or `.zip`).

Imported project structure has to be the following:
```text
pointcloud_project folder or .tar/.zip archive   
├── key_id_map.json (optional)              
├── meta.json     
├── dataset1                        
│ ├── pointcloud                    
│ │ ├── scene_1.pcd           
│ │ ├── scene_2.pcd   
│ │ └── ...                
│ ├── related_images                
│ │   ├── scene_1_pcd               
│ │   │ ├── scene_1_cam0.png       
│ │   │ ├── scene_1_cam0.png.json  
│ │   │ ├── scene_1_cam1.png       
│ │   │ ├── scene_1_cam1.png.json  
│ │   │ └── ... 
│ │   ├── scene_2_pcd               
│ │   │ ├── scene_2_cam0.png       
│ │   │ ├── scene_2_cam0.png.json  
│ │   │ ├── scene_2_cam1.png       
│ │   │ ├── scene_2_cam1.png.json  
│ │   │ └── ... 
│ │   └── ...      
│ └── ann
│     ├── scene_1.pcd.json
│     ├── scene_2.pcd.json
│     └── ...     
├── dataset2                       
│ ├── pointcloud                    
│ │ ├── scene_1.pcd
│ │ └── ...                
│ ├── related_images                
│ │   ├── scene_1_pcd               
│ │   │ ├── scene_1_cam0.png       
│ │   │ ├── scene_1_cam0.png.json  
│ │   │ ├── scene_1_cam1.png       
│ │   │ ├── scene_1_cam1.png.json  
│ │   │ └── ... 
│ │   └── ...      
│ └── ann
│     ├── scene_1.pcd.json
│     └── ...                      
└── dataset...                       
```


# How To Use 

1. Run app [Import Pointcloud Project](https://ecosystem.supervise.ly/apps/import-pointcloud-project) from ecosystem or from the context menu of directory or archive in **Team Files** -> `Run app` -> `Import pointcloud project`

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/import-pointcloud-project" src="https://user-images.githubusercontent.com/97401023/193620195-6481801e-0fc5-4ac3-858f-cb3a294defac.png" width="400px" style='padding-bottom: 10px'/>  

2. Wait for the app to import your data (project will be created in the current workspace)

# Demo Projects

You can export these projects from ecosystem with [`Export pointclouds project in Supervisely format`](https://ecosystem.supervise.ly/apps/export-pointclouds-project-in-supervisely-format) app to see examples of project structure.

- [Demo pointcloud project](https://ecosystem.supervise.ly/projects/demo-pointcloud-project)

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/demo-pointcloud-project" src="https://user-images.githubusercontent.com/97401023/193617265-431aa000-ae57-4beb-aa9b-8ba31d755b74.png" width="300px" margin-bottom="10px"/>  

- [Demo pointcloud project with labels](https://ecosystem.supervise.ly/projects/demo-pointcloud-project-annotated)

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/demo-pointcloud-project-annotated" src="https://user-images.githubusercontent.com/97401023/193617359-2b929837-901e-4d98-92b8-cecb32d8f3af.png" width="300px" margin-bottom="10px" />
