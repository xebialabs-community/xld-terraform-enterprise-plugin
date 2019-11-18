# Copyright 2019 XEBIALABS
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

from .workspaces import TFEWorkspaces
from .organizations import TFEOrganizations
from .config_versions import TFEConfigVersions
from .variables import TFEVariables
from .runs import TFERuns
from .state_versions import TFEStateVersions

class InvalidTFETokenException(Exception):
    """Cannot instantiate TFE Api class without a valid TFE_TOKEN."""


class TFE():
    """
    Super class for access to all TFE Endpoints.
    """

    def __init__(self, api_token, url):
        if api_token is None:
            raise InvalidTFETokenException
        TFE.configure_logger_stdout()

        self._instance_url = "{url}/api/v2".format(url=url)
        self._token = api_token
        self._current_organization = None
        self._headers = {
            "Authorization": "Bearer {0}".format(api_token),
            "Content-Type": "application/vnd.api+json"
        }
        self.config_versions = None
        self.variables = None
        self.runs = None
        self.state_versions = None
        self.organizations = TFEOrganizations( self._instance_url, None, self._headers)

    def set_organization(self, organization_name):
        """
        Sets the organization to use for org specific endpoints.
        This method must be called for their respective endpoints to work.
        """
        self._current_organization = organization_name
        self.workspaces = TFEWorkspaces(
            self._instance_url, self._current_organization, self._headers)
        self.config_versions = TFEConfigVersions(
            self._instance_url, self._current_organization, self._headers)
        self.variables = TFEVariables(
            self._instance_url, self._current_organization, self._headers)
        self.runs = TFERuns(self._instance_url,
                            self._current_organization, self._headers)
        self.state_versions = TFEStateVersions(
            self._instance_url, self._current_organization, self._headers)

    initializedLogger = 0

    @staticmethod
    def configure_logger_stdout():
        if TFE.initializedLogger == 0:
            import logging
            import sys
            root = logging.getLogger()
            root.setLevel(logging.DEBUG)

            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            root.addHandler(handler)
            TFE.initializedLogger = 1

