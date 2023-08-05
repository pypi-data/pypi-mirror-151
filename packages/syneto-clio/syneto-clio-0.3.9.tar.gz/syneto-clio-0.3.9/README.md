# Clio
An easy to use CLI tool for running faster kubernetes and docker commands.


<h2>Usage example</h2>

For seeing the logs of a kube pod or a service:

**$ syneto-clio logs <project_name>**

For entering a kube pod:

**$ syneto-clio enter <pod_name>**

For getting the status of all kube pods:

**$ syneto-clio check**

For restarting a docker container or a service:

**$ syneto-clio restart <project_name>**

For cleaning up hanging containers & images:

**$ syneto-clio cleanup docker**

For syncing the code of a project:

**$ syneto-clio sync <project_name>**

For mounting giove code:

_Sidenote:_ If you ran **config** command already, you can skip name, password and ip parameters and just provide the source path.

**$ syneto-clio sync giove --name < name > --password < password > --ip < ip_address > < source_path > **



