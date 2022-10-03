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

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/export-pointclouds-project-in-supervisely-format" src="" width="450px" style='padding-bottom: 20px'/>

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

1. Run app [Import Supervisely pointcloud episodes](https://ecosystem.supervise.ly/apps/import-pointcloud-episode) from ecosystem or from the context menu of directory or archive in **Team Files** -> `Run app` -> `Import pointcloud episodes in supervisely format`

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/import-pointcloud-project" src="" width="450px" style='padding-bottom: 20px'/>  

2. Wait for the app to import your data (project will be created in the current workspace)

<img src=""/>  

# Demo Projects

You can export these projects from ecosystem with [`Export pointclouds project in Supervisely format`](https://ecosystem.supervise.ly/apps/export-pointclouds-project-in-supervisely-format) app to see examples of project structure.

- [Demo pointcloud project](https://ecosystem.supervise.ly/projects/demo-pointcloud-project)

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/demo-pointcloud-project" src="" height="70px" margin-bottom="20px"/>  

- [Demo pointcloud project with labels](https://ecosystem.supervise.ly/projects/demo-pointcloud-project-annotated)

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/demo-pointcloud-project-annotated" src="" height="70px" margin-bottom="20px" />
