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
Module for Terraform Enterprise API Endpoint: Workspaces.
"""

import json
import requests

from .endpoint import TFEEndpoint

class TFEWorkspaces(TFEEndpoint):
    """
    Workspaces represent running infrastructure managed by Terraform.

    https://www.terraform.io/docs/enterprise/api/workspaces.html
    """

    def __init__(self, base_url, organization_name, headers,proxy_server):
        super(TFEWorkspaces,self).__init__(base_url, organization_name, headers, proxy_server)
        self._ws_base_url = "{base_url}/workspaces".format(base_url=base_url)
        self._org_base_url = "{base_url}/organizations/{organization_name}/workspaces".format(base_url=base_url, organization_name=organization_name)

    def create(self, workspace_name, terraform_version = "0.12.9"):
        """
        POST /organizations/:organization_name/workspaces
        """
        payload = {
                "data": {
                    "attributes": {
                        "name": workspace_name,
                        "auto-apply":"true",
                        "terraform-version": terraform_version
                        },
                    "type": "workspaces"
                    }
                }
        return self._create(self._org_base_url, payload)

    def destroy(self, workspace_id=None, workspace_name=None):
        """
        GET /organizations/:organization_name/workspaces/:name
        DELETE /workspaces/:workspace_id

        A workspace can be deleted via two endpoints, which behave identically. One refers to a
        workspace by its ID, and the other by its name and organization.
        """
        if workspace_name is not None:
            url = "{0}/{1}".format(self._org_base_url, workspace_name)
        elif workspace_id is not None:
            url = "{0}/{1}".format(self._ws_base_url,workspace_id)
        else:
            self._logger.error("Arguments workspace_name or workspace_id must be defined")

        return self._destroy(url)

    def show(self, workspace_name=None, workspace_id=None):
        """
        GET /organizations/:organization_name/workspaces/:name
        GET /workspaces/:workspace_id

        Details on a workspace can be retrieved from two endpoints, which behave identically.
        One refers to a workspace by its ID, and the other by its name and organization.
        """
        if workspace_name is not None:
            url = "{0}/{1}".format(self._org_base_url, workspace_name)
        elif workspace_id is not None:
            url = "{0}/{1}".format(self._ws_base_url,workspace_id)
        else:
            self._logger.error("Arguments workspace_name or workspace_id must be defined")

        return self._show(url)
    
    def get_id(self, workspace_name):
        workspace = self.show(workspace_name=workspace_name)
        ws_id = workspace["data"]["id"]
        self._logger.info("workspace {0} -> id {1}".format(workspace_name,ws_id))
        return ws_id

    def lst(self):
        """
        GET /organizations/:organization_name/workspaces

        This endpoint lists workspaces in the organization.
        """
        return self._ls(self._org_base_url)

