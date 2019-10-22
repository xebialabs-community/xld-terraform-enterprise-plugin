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

    def __init__(self, base_url, organization_name, headers):
        super(TFEStateVersions,self).__init__(base_url, organization_name, headers)
        self._state_version_base_url = "{base_url}/state-versions".format(base_url=base_url)
        self._workspace_base_url = "{base_url}/workspaces".format(base_url=base_url)

    def get_current(self, workspace_id):
        """
        GET /workspaces/:workspace_id/current-state-version

        Fetches the current state version for the given workspace. This state version will be
        the input state when running terraform operations.
        """
        results = None
        url = "{0}/{1}/current-state-version".format(self._workspace_base_url,workspace_id)
        req = requests.get(url, headers=self._headers, verify=self._verify)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def get_current_state_content(self, url):
        results = None
        req = requests.get(url, headers=self._headers, verify=self._verify)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def show(self, state_version_id):
        """
        GET /state-versions/:state_version_id
        """
        url = "{0}/{1}".format(self._state_version_base_url,state_version_id)
        return self._show(url)
