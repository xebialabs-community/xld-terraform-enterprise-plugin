from terraxld.api import TFE
import glob
import tarfile
import os
from com.xebialabs.overthere.local import LocalFile,LocalConnection

def tar_directory(source_dir):
    archive_file = LocalConnection.getLocalConnection().getTempFile("tfe-xld.tgz")
    print(archive_file)
    print(archive_file.path)

    tar = tarfile.open(archive_file.path, "w:gz")
    for file_name in glob.glob(os.path.join(source_dir, "*")):
        print("  Adding %s..." % file_name)
        tar.add(file_name, os.path.basename(file_name))
    tar.close()
    return archive_file


artifact=deployed.file.path
archive_file = tar_directory(artifact)
print("TGZ:"+archive_file.path)


organization = deployed.container.organization
myapi = TFE(api_token=organization.token, url=organization.url)
myapi.set_organization(organization.name)
workspace_name = deployed.workspaceName

workspace = myapi.workspaces.show(workspace_name=workspace_name)
ws_id = workspace["data"]["id"]

config_version=myapi.config_versions.create(ws_id)['data']
cv_id = config_version["id"]
print("New configuration version {0}".format(cv_id))

print("upload the tgz")
myapi.config_versions.upload(archive_file.path,cv_id)
context.setAttribute(deployed.name+"_cv_id", cv_id)



