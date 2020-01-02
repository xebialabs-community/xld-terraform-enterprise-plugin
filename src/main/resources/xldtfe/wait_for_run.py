    #
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
from java.lang import System
from terraxld.api import TFE
import os
import sys
import json
import time

def dump_json(data, message):
    if True:
        print(50*'=')
        print(message)
        print(50*'=')
        json.dump(data, sys.stdout, indent=4)
        print(50*'=')

def stream_plan_output(myapi,run_id, message):
    #TODO: use the stream api to dump the archivist logs continuously
    print(50*'=')
    print(message)
    print(50*'=')
    s_plan = myapi.runs.show_plan(run_id)
    status = s_plan['data']['attributes']['status']
    archivist_url = s_plan['data']['attributes']['log-read-url']
    while status == 'running':
        print "--> status {0}".format(status)
        time.sleep(5)
        s_plan = myapi.runs.show_plan(run_id)
        status = s_plan['data']['attributes']['status']

    print(50*'=')
    if status  == 'errored':
        [sys.stderr.write(line+"\n") for line in myapi.runs.show_plan_log(run_id).split('\n')]
        raise Exception("Error during the plan phase")
    if status  == 'finished':
        print myapi.runs.show_plan_log(run_id)
    print(50*'=')


def stream_apply_output(myapi,run_id, message):
    #TODO: use the stream api to dump the archivist logs continuously
    print(50*'=')
    print(message)
    print(50*'=')
    s_apply = myapi.runs.show_apply(run_id)
    status = s_apply['data']['attributes']['status']
    archivist_url = s_apply['data']['attributes']['log-read-url']
    while status == 'running':
        print "--> status {0}".format(status)
        time.sleep(5)
        s_apply = myapi.runs.show_apply(run_id)
        status = s_apply['data']['attributes']['status']

    print(50*'=')
    if status  == 'errored':
        [sys.stderr.write(line+"\n") for line in myapi.runs.show_apply_log(run_id).split('\n')]
        raise Exception("Error during the Apply phase")
    if status  == 'finished':
        print myapi.runs.show_apply_log(run_id)
    print(50*'=')




myapi = TFE(deployed.container.organization)


while True:
    run_id = context.getAttribute(deployed.name+"_run_id")
    run=myapi.runs.show(run_id)['data']
    #dump_json(run,"run")
    run_status = run['attributes']['status']
    print("run_status: {0}     {1}".format(run_id, run_status))

    if run_status == 'planning':
        stream_plan_output(myapi,run_id, "Plan Log {0}/{1}".format(run_status,run_id))

    if run_status == 'applying':
        stream_apply_output(myapi,run_id, "Apply Log {0}/{1}".format(run_status,run_id))

    if run_status == 'applied' or run_status == 'planned_and_finished':
        print("done")
        break
    elif run_status == 'errored':
        stream_plan_output(myapi,run_id, "Plan Log {0}/{1}".format(run_status,run_id))
        raise Exception("An error occured in  {0}".format(run_id))

    time.sleep(1)

