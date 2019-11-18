#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

"""
Module for Terraform Enterprise API Endpoint: Config Versions.
"""

import json
import requests

from .endpoint import TFEEndpoint

class TFEConfigVersions(TFEEndpoint):
    """
    A configuration version (configuration-version) is a resource used to reference the
    uploaded configuration files. It is associated with the run to use the uploaded configuration
    files for performing the plan and apply.

    https://www.terraform.io/docs/enterprise/api/configuration-versions.html
    """

    def __init__(self, base_url, organization_name, headers):
        super(TFEConfigVersions,self).__init__(base_url, organization_name, headers)
        self._ws_base_url = "{0}/workspaces".format(base_url)
        self._config_version_base_url = "{0}/configuration-versions".format(base_url)

    def lst(self, workspace_id, page_number=None, page_size=None):
        """
        GET /workspaces/:workspace_id/configuration-versions

        This endpoint supports pagination with standard URL query parameters; remember to
        percent-encode.
        """
        url = "{0}/{1}/configuration-versions".format(self._ws_base_url,workspace_id)

        filters = []
        if page_number is not None:
            filters.append("page[number]={page_number}".format(page_number=page_number))

        if page_size is not None:
            filters.append("page[size]={page_size}".format(page_size=page_size))

        if filters:
            url += "?" + "&".join(filters)

        return self._ls(url)

    def show(self, config_version_id):
        """
        GET /configuration-versions/:configuration-config_version_id
        """
        url = "{0}/{1}".format(self._config_version_base_url,config_version_id)
        return self._show(url)

    def create(self, workspace_id):
        """
        POST /workspaces/:workspace_id/configuration-versions

        This POST endpoint requires a JSON object with the following properties as a request
        payload.

        Properties without a default value are required.
        """

        payload = {
                "data": {
                    "type": "configuration-versions",
                    "attributes": {
                        "auto-queue-runs": 'false'
                        }
                    }
                }

        url = "{0}/{1}/configuration-versions".format(self._ws_base_url,workspace_id)
        return self._create(url, payload)

    def upload(self, path_to_tarball, config_version_id):
        """
        PUT {derived_config_version_upload_url}
        """
        results = None
        # TODO: Validate the path to tarball a bit
        upload_url = self.show(config_version_id)["data"]["attributes"]["upload-url"]

        # TODO: Exception and error handling
        req = None
        with open(path_to_tarball, 'rb') as data:
            req = requests.put(upload_url, data=data, headers=self._headers, verify=self._verify)

        if req.status_code == 200:
            self._logger.debug("Config version successfully uploaded.")
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results
