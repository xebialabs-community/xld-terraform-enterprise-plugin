from terraxld.api import TFE
import os

organization = deployed.container.organization
myapi = TFE(api_token=organization.token, url=organization.url)
myapi.set_organization(organization.name)
workspace_name = deployed.workspaceName

workspace = myapi.workspaces.show(workspace_name=workspace_name)
ws_id = workspace["data"]["id"]
print("workspace {0},id {1}".format(workspace_name,ws_id))

for key in deployed.inputVariables:
    value = deployed.inputVariables[key]
    print("new terraform variable {0} -> {1}".format(key,value))
    myapi.variables.create(ws_id,key,value,'terraform','false')

for key in deployed.secretInputVariables:
    value = deployed.secretInputVariables[key]
    print("new terraform secret variable {0} -> {1}".format(key,'xxxxxxxx'))
    myapi.variables.create(ws_id,key,value,'terraform','true')
