#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

"""
Module for Terraform Enterprise API Endpoint: State Versions.
"""

import json
import requests

from .endpoint import TFEEndpoint


class TFEStateVersions(TFEEndpoint):
    """
    https://www.terraform.io/docs/enterprise/api/state-versions.html
    """

    def __init__(self, base_url, organization, headers):
        super(TFEStateVersions, self).__init__(base_url, organization, headers)
        self._state_version_base_url = "{base_url}/state-versions".format(base_url=base_url)
        self._workspace_base_url = "{base_url}/workspaces".format(base_url=base_url)

    def get_current(self, workspace_id):
        """
        GET /workspaces/:workspace_id/current-state-version

        Fetches the current state version for the given workspace. This state version will be
        the input state when running terraform operations.
        """
        results = None
        url = "{0}/{1}/current-state-version".format(self._workspace_base_url, workspace_id)
        self._logger.debug(url)
        req = requests.get(url, headers=self._headers, verify=self._verify, proxies=self._proxies)

        if req.status_code == 200:
            results = json.loads(req.content)
            return results
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            return err

    def get_current_state_content(self, url):
        return json.loads(self._download(url))

    def show(self, state_version_id):
        """
        GET /state-versions/:state_version_id
        """
        url = "{0}/{1}".format(self._state_version_base_url, state_version_id)
        return self._show(url)

    def get_current_state_content_workspace(self, ws_id):
        sv_current = self.get_current(ws_id)
        print(sv_current)
        if 'errors' in sv_current:
            raise Exception("error when getting the state of the workspace {0}".format(sv_current))

        self._logger.debug(sv_current)
        sv_id = sv_current["data"]["id"]
        print("..current state version {0}".format(sv_id))

        state_file_url = sv_current["data"]["attributes"]["hosted-state-download-url"]

        print("..current state file {0}".format(state_file_url))
        output = json.loads(self._download(state_file_url))
        return output
