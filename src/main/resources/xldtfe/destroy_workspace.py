from terraxld.api import TFE
import os

organization = previousDeployed.container.organization
myapi = TFE(api_token=organization.token, url=organization.url)
myapi.set_organization(organization.name)
workspace_name =  previousDeployed.workspaceName
print("destroy a workspace {0}".format(workspace_name))
workspace=myapi.workspaces.destroy(workspace_name=workspace_name)
print(workspace)


