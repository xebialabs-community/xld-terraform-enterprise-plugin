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
Module for container class of all TFE endpoints and high level exceptions around
API access.
"""

import terraxld.variables
reload(terraxld.variables)

from .workspaces import TFEWorkspaces
from .organizations import TFEOrganizations
from .config_versions import TFEConfigVersions
from .variables import TFEVariables
from .runs import TFERuns
from .state_versions import TFEStateVersions
from .hclparser import  HclParser

class InvalidTFETokenException(Exception):
    """Cannot instantiate TFE Api class without a valid TFE_TOKEN."""


class TFE():
    """
    Super class for access to all TFE Endpoints.
    """

    def __init__(self,organization):
        self.organization = organization
        if self.organization.token is None:
            raise InvalidTFETokenException

        TFE.configure_logger_stdout(self.organization.debug)

        self._instance_url = "{url}/api/v2".format(url=self.organization.url)
        self._token = self.organization.token
        self._current_organization = None
        self._headers = {
            "Authorization": "Bearer {0}".format(self.organization.token),
            "Content-Type": "application/vnd.api+json"
        }
        self.config_versions = None
        self.variables = None
        self.runs = None
        self.state_versions = None
        self.organizations = TFEOrganizations( self._instance_url, None, self._headers, self.organization.proxyServer)
        if self.organization.organizationName is not None:
            self._set_organization(self.organization.organizationName)
        else:
            self._set_organization(self.organization.name)

        self.hcl_parser = HclParser()

    def _set_organization(self, organization_name):
        """
        Sets the organization to use for org specific endpoints.
        This method must be called for their respective endpoints to work.
        """
        self._current_organization = organization_name
        self.workspaces = TFEWorkspaces(
            self._instance_url, self._current_organization, self._headers, self.organization.proxyServer)
        self.config_versions = TFEConfigVersions(
            self._instance_url, self._current_organization, self._headers, self.organization.proxyServer)
        self.variables = TFEVariables(
            self._instance_url, self._current_organization, self._headers, self.organization.proxyServer)
        self.runs = TFERuns(
            self._instance_url, self._current_organization, self._headers, self.organization.proxyServer)
        self.state_versions = TFEStateVersions(
            self._instance_url, self._current_organization, self._headers, self.organization.proxyServer)

    log_handler = None

    @staticmethod
    def configure_logger_stdout(debug):
        import logging
        import sys
        root = logging.getLogger()
        if TFE.log_handler == None:
            handler = logging.StreamHandler(sys.stdout)
            TFE.log_handler = handler
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            root.addHandler(handler)
        else:
            handler = TFE.log_handler

        if debug:
            root.setLevel(logging.DEBUG)
            handler.setLevel(logging.DEBUG)
        else:
            root.setLevel(logging.INFO)
            handler.setLevel(logging.INFO)


    def load_variables_in_workspace(self,input,ws_name, secret, scope):
        ws_id = self.workspaces.get_id(ws_name)
        data = self.variables.lst(workspace_name=ws_name)
        existing_variables = {}
        for variable_info in data['data']:
            existing_variables[variable_info['attributes']['key']] = variable_info['id']

        for key in input:
            value = input[key]
            is_hcl = self.hcl_parser.is_hcl_variable(key)
            if key in existing_variables:
                print("update terraform variable {0} -> {1} ({2})".format(key, self.display_value(value,secret), is_hcl))
                if secret:
                    self.variables.destroy(existing_variables[key])
                    self.variables.create(ws_id, key, value, scope, secret, is_hcl)
                else:
                    self.variables.update(existing_variables[key], key, value, scope, secret, is_hcl)
            else:
                print("new terraform variable {0} -> {1} ({2})".format(key, self.display_value(value,secret), is_hcl))
                self.variables.create(ws_id, key, value, scope, secret, is_hcl)

    def display_value(self, value, secret):
        if secret:
            return 'xxxxxxxxxxxxxx'
        else:
            return value