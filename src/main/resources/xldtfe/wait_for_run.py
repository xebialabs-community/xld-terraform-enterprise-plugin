from terraxld.api import TFE
import os

organization = deployed.container.organization
myapi = TFE(api_token=organization.token, url=organization.url)
myapi.set_organization(organization.name)

run_id = context.getAttribute(deployed.name+"_run_id")
run=myapi.runs.show(run_id)['data']
run_id = run['id']
run_status = run['attributes']['status']
print("{0}     {1}".format(run_id, run_status))
if run_status == 'applied':
    print "done"
else:
    result = "RETRY"
