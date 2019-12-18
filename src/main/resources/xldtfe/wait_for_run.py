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

myapi = TFE(deployed.container.organization)

run_id = context.getAttribute(deployed.name+"_run_id")
print("run_id {0}".format(run_id))
run=myapi.runs.show(run_id)['data']
run_id = run['id']
if deployed.container.organization.debug:
    print(50*'-')
    json.dump(run, sys.stdout, indent=4)
    print(50*'-')

run_status = run['attributes']['status']
print("{0}     {1}".format(run_id, run_status))
if run_status == 'applied' or run_status == 'planned_and_finished':
    print("done")
elif run_status == 'errored':
    raise Exception("An error occured in  {0}".format(run_id))
else:
    result = "RETRY"
