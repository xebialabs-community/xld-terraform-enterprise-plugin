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

myapi = TFE(previousDeployed.container.organization)
workspace_name = previousDeployed.workspaceName
ws_id = myapi.workspaces.get_id(workspace_name)

cv_id = context.getAttribute(previousDeployed.name+"_cv_id")
print("cv_id {0}".format(cv_id))
task_id = context.getTask().getId()
run = myapi.runs.destroy(ws_id,cv_id,"Trigger Destroy by XLDeploy {0}".format(task_id))['data']
run_id = run['id']
context.setAttribute(previousDeployed.name+"_run_id", run_id)
print("run id is {0}".format(run_id))

