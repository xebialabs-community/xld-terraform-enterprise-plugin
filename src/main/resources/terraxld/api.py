"""
Module for container class of all TFE endpoints and high level exceptions around
API access.
"""

from .workspaces import TFEWorkspaces
from .organizations import TFEOrganizations
from .config_versions import TFEConfigVersions
from .variables import TFEVariables
from .runs import TFERuns

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

