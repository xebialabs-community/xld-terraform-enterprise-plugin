from terraxld.api import TFE
import os

organization = deployed.container.organization
myapi = TFE(api_token=organization.token, url=organization.url)
myapi.set_organization(organization.name)
workspace_name = deployed.workspaceName
print("create a new workspace {0}".format(workspace_name))
workspace=myapi.workspaces.create(workspace_name)
ws_id = workspace["data"]["id"]
print("Workspace id {0}".format(ws_id))

print(myapi.workspaces.show(workspace_id=ws_id))
print(myapi.workspaces.show(workspace_name=workspace_name))

