# Clio
An easy to use CLI tool for running faster Kubernetes and Docker commands.

<h2>Usage example</h2>

>For seeing the logs of a kubernetes pod or a system service:
>
>**$ syneto-clio logs <project_name>**


>For entering a kubernetes pod:
>
>**$ syneto-clio enter <pod_name>**


>For getting the status of all kubernetes pods:
>
>**$ syneto-clio check**


>For restarting a docker container or a system service:
>
>**$ syneto-clio restart <project_name>**


>For cleaning up hanging containers & images:
>
>**$ syneto-clio cleanup docker**


>For syncing the code of a project:
>
>**$ syneto-clio sync <project_name> --name < name > --password < password > --ip < ip_address >  < source_path >**
>
>_Sidenote:_ If you ran **config** command already, you can skip name, password and ip parameters and just provide the source path.

