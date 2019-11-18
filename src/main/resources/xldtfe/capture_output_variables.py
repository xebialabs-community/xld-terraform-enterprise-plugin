#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

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
