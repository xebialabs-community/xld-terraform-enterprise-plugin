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

    def __init__(self, base_url, organization_name, headers):
        super(TFEWorkspaces,self).__init__(base_url, organization_name, headers)
        self._ws_base_url = "{base_url}/workspaces".format(base_url=base_url)
        self._org_base_url = "{base_url}/organizations/{organization_name}/workspaces".format(base_url=base_url, organization_name=organization_name)

    def create(self, workspace_name):
        """
        POST /organizations/:organization_name/workspaces
        """
        payload = {'data': {'attributes':{'name':workspace_name},'type':'workspace'}}
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

