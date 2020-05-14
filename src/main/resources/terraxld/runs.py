#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import requests

from .endpoint import TFEEndpoint


class TFERuns(TFEEndpoint):
    """
    Performing a run on a new configuration is a multi-step process.

    Create a configuration version on the workspace.
    Upload configuration files to the configuration version.
    Create a run on the workspace; this is done automatically when a config file is uploaded.
    Create and queue an apply on the run; if the run can't be auto-applied.

    Alternatively, you can create a run with a pre-existing configuration version, even one from
    another workspace. This is useful for promoting known good code from one workspace to another.

    https://www.terraform.io/docs/enterprise/api/run.html
    """

    def __init__(self, base_url, organization, headers):
        super(TFERuns, self).__init__(base_url, organization, headers)
        self._ws_base_url = "{base_url}/workspaces".format(base_url=base_url)
        self._runs_base_url = "{base_url}/runs".format(base_url=base_url)

    def show(self, run_id):
        """
        GET /runs/:run_id

        This endpoint is used for showing details of a specific run.
        """
        url = "{0}/{1}".format(self._runs_base_url, run_id)
        return self._show(url)

    def show_plan(self, run_id):
        """
        GET /runs/:run_id/plan

        This endpoint is used for showing details of the plan of a specific run.
        """
        url = "{0}/{1}/plan".format(self._runs_base_url, run_id)
        return self._show(url)

    def show_plan_log(self, run_id):
        s_plan = self.show_plan(run_id)
        archivist_url = s_plan['data']['attributes']['log-read-url']
        return self._download(archivist_url)

    def stream_plan_log(self, run_id):
        s_plan = self.show_plan(run_id)
        archivist_url = s_plan['data']['attributes']['log-read-url']
        return self._stream(archivist_url)

    def show_apply(self, run_id):
        """
        GET /runs/:run_id/apply

        This endpoint is used for showing details of the apply of a specific run.
        """
        url = "{0}/{1}/apply".format(self._runs_base_url, run_id)
        return self._show(url)

    def show_apply_log(self, run_id):
        s_apply = self.show_apply(run_id)
        archivist_url = s_apply['data']['attributes']['log-read-url']
        return self._download(archivist_url)

    def stream_apply_log(self, run_id):
        s_apply = self.show_apply(run_id)
        archivist_url = s_apply['data']['attributes']['log-read-url']
        return self._stream(archivist_url)

    def create(self, ws_id, config_id, message):
        """
        POST /runs

        A run performs a plan and apply, using a configuration version and the workspaces
        current variables. You can specify a configuration version when creating a run; if
        you don't provide one, the run defaults to the workspace's most recently used version.
        """

        payload = {
            "data": {
                "attributes": {
                    "is-destroy": "false",
                    "message": message
                },
                "type": "runs",
                "relationships": {
                    "workspace": {
                        "data": {
                            "type": "workspaces",
                            "id": ws_id
                        }
                    },
                    "configuration-version": {
                        "data": {
                            "type": "configuration-versions",
                            "id": config_id
                        }
                    }
                }
            }
        }

        self._logger.debug(json.dumps(payload))
        return self._create(self._runs_base_url, payload)

    def destroy(self, ws_id, config_id, message):
        """
        POST /runs

        A run performs a plan and apply, using a configuration version and the workspace's
        current variables. You can specify a configuration version when creating a run; if
        you don't provide one, the run defaults to the workspace's most recently used version.
        """

        payload = {
            "data": {
                "attributes": {
                    "is-destroy": "true",
                    "message": message
                },
                "type": "runs",
                "relationships": {
                    "workspace": {
                        "data": {
                            "type": "workspaces",
                            "id": ws_id
                        }
                    },
                    "configuration-version": {
                        "data": {
                            "type": "configuration-versions",
                            "id": config_id
                        }
                    }
                }
            }
        }

        self._logger.debug(json.dumps(payload))
        return self._create(self._runs_base_url, payload)

    def apply(self, run_id):
        """
        POST /runs/:run_id/actions/apply

        Applies a run that is paused waiting for confirmation after a plan. This includes runs
        in the "needs confirmation" and "policy checked" states. This action is only required for
        runs that can't be auto-applied. (Plans can be auto-applied if the auto-apply setting is
        enabled on the workspace, the plan is not a destroy plan, and the plan was not queued by a
        user without write permissions.)

        This endpoint queues the request to perform an apply; the apply might not happen
        immediately.

        This endpoint represents an action as opposed to a resource. As such, the endpoint does
        not return any object in the response body.
        """
        url = "{0}/{1}/actions/apply".format(self._runs_base_url, run_id)
        req = requests.post(url, headers=self._headers, proxies=self._proxies)

        if req.status_code == 202:
            self._logger.debug("Run successfully applied.")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

    def discard(self, run_id):
        """
        POST /runs/:run_id/actions/discard

        The discard action can be used to skip any remaining work on runs that are paused
        waiting for confirmation or priority. This includes runs in the "pending,"
        "needs confirmation," "policy checked," and "policy override" states.

        This endpoint queues the request to perform a discard; the discard might not happen
        immediately. After discarding, the run is completed and later runs can proceed.

        This endpoint represents an action as opposed to a resource. As such, it does not
        return any object in the response body.
        """
        url = "{0}/{1}/actions/discard".format(self._runs_base_url, run_id)
        req = requests.post(url, headers=self._headers, proxies=self._proxies)

        if req.status_code == 202:
            self._logger.debug("Run successfully discarded.")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

    def cancel(self, run_id):
        """
        POST /runs/:run_id/actions/cancel

        The cancel action can be used to interrupt a run that is currently planning or applying.
        Performing a cancel is roughly equivalent to hitting ctrl+c during a Terraform plan or
        apply on the CLI. The running Terraform process is sent an INT signal, which instructs
        Terraform to end its work and wrap up in the safest way possible.

        This endpoint queues the request to perform a cancel; the cancel might not happen
        immediately. After canceling, the run is completed and later runs can proceed.

        This endpoint represents an action as opposed to a resource. As such, it does not
        return any object in the response body.
        """
        url = "{0}/{1}/actions/cancel".format(self._runs_base_url, run_id)
        req = requests.post(url, headers=self._headers, proxies=self._proxies)

        if req.status_code == 202:
            self._logger.debug("Run successfully canceled.")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

    def force_cancel(self, run_id):
        """
        POST /runs/:run_id/actions/force-cancel

        The force-cancel action is like cancel, but ends the run immediately. Once invoked,
        the run is placed into a canceled state, and the running Terraform process is terminated.
        The workspace is immediately unlocked, allowing further runs to be queued. The force-cancel
        operation requires workspace admin privileges.

        This endpoint enforces a prerequisite that a non-forceful cancel is performed first, and a
        cool-off period has elapsed. To determine if this criteria is met, it is useful to check
        the data.attributes.is-force-cancelable value of the run details endpoint. The time at
        which the force-cancel action will become available can be found using the run details
        endpoint, in the key data.attributes.force_cancel_available_at. Note that this key is only
        present in the payload after the initial cancel has been initiated.

        This endpoint represents an action as opposed to a resource. As such, it does not return any
        object in the response body.
        """
        url = "{0}/{1}/actions/force-cancel".format(self._runs_base_url, run_id)
        req = requests.post(url, headers=self._headers, proxies=self._proxies)

        if req.status_code == 202:
            self._logger.debug("Run successfully force canceled.")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

    def force_execute(self, run_id):
        """
        POST /runs/:run_id/actions/force-execute

        The force-execute action cancels all prior runs that are not already complete, unlocking
        the run's workspace and allowing the run to be executed. (It initiates the same actions
        as the "Run this plan now" button at the top of the view of a pending run.)

        This endpoint enforces the following prerequisites:
            The target run is in the "pending" state.
            The workspace is locked by another run.
            The run locking the workspace can be discarded.

        This endpoint represents an action as opposed to a resource. As such, it does not return any
        object in the response body.
        """
        url = "{0}/{1}/actions/force-execute".format(self._runs_base_url, run_id)
        req = requests.post(url, headers=self._headers, proxies=self._proxies)

        if req.status_code == 202:
            self._logger.debug("Run successfully force executed.")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
