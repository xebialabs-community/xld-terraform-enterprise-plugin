from terraxld.api import TFE
import os

organization = deployed.container.organization
myapi = TFE(api_token=organization.token, url=organization.url)
myapi.set_organization(organization.name)
workspace_name = deployed.workspaceName

workspace = myapi.workspaces.show(workspace_name=workspace_name)
ws_id = workspace["data"]["id"]
print("workspace {0},id {1}".format(workspace_name,ws_id))
cv_id = context.getAttribute(deployed.name+"_cv_id")
print("cv_id {0}".format(cv_id))
task_id = context.getTask().getId()
run = myapi.runs.create(ws_id,cv_id,"Trigger by XLDeploy {0}".format(task_id))['data']
run_id = run['id']
context.setAttribute(deployed.name+"_run_id", run_id)
print("run id is {0}".format(run_id))

