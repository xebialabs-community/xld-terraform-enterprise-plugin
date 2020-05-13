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
from org.apache.commons.io import IOUtils
from java.nio.charset import Charset

from org.apache.http.impl.client import HttpClientBuilder
from org.apache.http.client.methods import HttpGet
from org.apache.http.ssl import SSLContextBuilder
from org.apache.http.conn.ssl import TrustSelfSignedStrategy
from org.apache.http.conn.ssl import NoopHostnameVerifier


class TFEStateVersions(TFEEndpoint):
    """
    https://www.terraform.io/docs/enterprise/api/state-versions.html
    """

    def __init__(self, base_url, organization_name, headers, proxy_server):
        super(TFEStateVersions, self).__init__(base_url, organization_name, headers, proxy_server)
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
        req = requests.get(url, headers=self._headers, verify=self._verify, proxies=self._proxies)

        if req.status_code == 200:
            results = json.loads(req.content)
            return results
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            return err

    def get_current_state_content(self, url, dowload_method):
        # if XLD runs on Windows the (j)ython implementation raises an exception "java.util.zip.DataFormatException: invalid code lengths"
        # the bug seems coming from an error in the Local.
        # the "JAVA"  alternative implementation solves this and becomes the default implementation.
        # To control the download_method value modify the value in type system,
        # terraformEnterprise.Organization.downloadMethod set as hidden="true"
        self._logger.error("get_current_state_content {0}".format(url))
        if dowload_method == "PYTHON":
            req = requests.get(url, headers=self._headers, verify=self._verify, proxies=self._proxies)
            if req.status_code == 200:
                results = json.loads(req.content)
            else:
                err = json.loads(req.content.decode("utf-8"))
                self._logger.error(err)
            return results

        if dowload_method == "JAVA":
            http_client_builder = HttpClientBuilder.create()
            http_client_builder.setProxy(self._java_proxy)

            ssl_context = SSLContextBuilder().loadTrustMaterial(None, TrustSelfSignedStrategy()).build()
            http_client_builder.setSSLContext(ssl_context).setSSLHostnameVerifier(NoopHostnameVerifier())

            client = http_client_builder.build()
            http_response = client.execute(HttpGet(url))
            content = IOUtils.toString(http_response.getEntity().getContent(), Charset.forName("UTF-8"))
            return json.loads(content)

        raise Exception("{0} unknown ".format(dowload_method))

    def show(self, state_version_id):
        """
        GET /state-versions/:state_version_id
        """
        url = "{0}/{1}".format(self._state_version_base_url, state_version_id)
        return self._show(url)

    def get_current_state_content_workspace(self, ws_id, dowload_method):
        sv_current = self.get_current(ws_id)
        if 'errors' in sv_current:
            raise Exception("error when getting the state of the workspace {0}".format(sv_current))
        self._logger.info(sv_current)
        sv_id = sv_current["data"]["id"]
        print("..current state version {0}".format(sv_id))

        state_file_url = sv_current["data"]["attributes"]["hosted-state-download-url"]

        print("..current state file {0}".format(state_file_url))

        output = self.get_current_state_content(state_file_url, dowload_method)
        return output
