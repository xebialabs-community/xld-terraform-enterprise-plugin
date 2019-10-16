from terraxld.api import TFE

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
myapi.config_versions.upload('/tmp/terraform.tar.gz',cv_id)
context.setAttribute(deployed.name+"_cv_id", cv_id)


