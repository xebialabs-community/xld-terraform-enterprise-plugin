from terraxld.api import TFE
import os
import sys
import json

organization = deployed.container.organization
myapi = TFE(api_token=organization.token, url=organization.url)
myapi.set_organization(organization.name)
workspace_name = deployed.workspaceName

workspace = myapi.workspaces.show(workspace_name=workspace_name)
ws_id = workspace["data"]["id"]
print("workspace {0},id {1}".format(workspace_name,ws_id))

sv_current=myapi.state_versions.get_current(ws_id)

sv_id=sv_current["data"]["id"]
print("current state version {0}".format(sv_id))

state_file_url=sv_current["data"]["attributes"]["hosted-state-download-url"]

print("current state file {0}".format(state_file_url))

output = myapi.state_versions.get_current_state_content(state_file_url)

if output:
    output_variables = {}
    output_json = output['outputs']

    for key in output_json:
        output_variables[key] = output_json[key]['value']
        print("new output variable found {0}:{1}".format(key,output_variables[key]))
    deployed.outputVariables = output_variables
    context.logOutput("Output variables from Terraform captured.")
else:
    context.logOutput("No output variables found.")
