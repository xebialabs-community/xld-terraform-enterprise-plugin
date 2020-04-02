#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import terraxld.api
reload(terraxld.api)
from terraxld.api import TFE

myapi = TFE(deployed.container.organization)
workspace_name = deployed.workspaceName
ws_id = myapi.workspaces.get_id(workspace_name)
myapi.hcl_parser.parse_folder(deployed)

basics=dict()
basics['TF_CLI_ARGS']='-no-color'
basics['CONFIRM_DESTROY']='1'

non_secured_items = {}
non_secured_items.update(basics)
non_secured_items.update(deployed.container.variables)

secured_items = {}
secured_items.update(deployed.container.credentials)

for cpm_key in deployed.container.credentialsPropertyMapping:
    if cpm_key == "empty":
        continue
    key = deployed.container.credentialsPropertyMapping[cpm_key]
    value = deployed.container.getProperty(cpm_key)
    pd_key = deployed.container.type.getDescriptor().getPropertyDescriptor(cpm_key)
    if pd_key.isPassword():
        secured_items[key]=value
    else:
        non_secured_items[key]=value


myapi.load_variables_in_workspace(non_secured_items, workspace_name, False, scope='env')
myapi.load_variables_in_workspace(secured_items, workspace_name, True, scope='env')

