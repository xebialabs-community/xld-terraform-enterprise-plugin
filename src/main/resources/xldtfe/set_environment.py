#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from terraxld.api import TFE
import os

myapi = TFE(deployed.container.organization)
workspace_name = deployed.workspaceName
ws_id = myapi.workspaces.get_id(workspace_name)

# Inject -no-color options to get no formating in  the logs.
myapi.variables.create(ws_id,'TF_CLI_ARGS','-no-color','env','false')
myapi.variables.create(ws_id,'CONFIRM_DESTROY','1','env','false')

for cpm_key in deployed.container.credentialsPropertyMapping:
    if cpm_key == "empty":
        continue
    key = deployed.container.credentialsPropertyMapping[cpm_key]
    value = deployed.container.getProperty(cpm_key)
    pd_key = deployed.container.type.getDescriptor().getPropertyDescriptor(cpm_key)
    if pd_key.isPassword():
        print("new env sensitive variable {0} -> xxxxxxx".format(key))
        myapi.variables.create(ws_id,key,value,'env','true')
    else:
        print("new env variable {0} -> {1}".format(key,value))
        myapi.variables.create(ws_id,key,value,'env','false')

for key in deployed.container.variables:
    value = deployed.container.variables[key]
    print("new env variable {0} -> {1}".format(key,value))
    myapi.variables.create(ws_id,key,value,'env','false')


for key in deployed.container.credentials:
    value = deployed.container.credentials[key]
    print("new env sensitive variable {0} -> xxxxxxx".format(key))
    myapi.variables.create(ws_id,key,value,'env','true')
