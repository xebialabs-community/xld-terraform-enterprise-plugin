"""
Module for Terraform Enterprise API Endpoint: Organizations.
"""

import json
import requests

from .endpoint import TFEEndpoint

class TFEOrganizations(TFEEndpoint):
    """
    The Organizations API is used to list, show, create, update, and destroy organizations.

    https://www.terraform.io/docs/enterprise/api/organizations.html
    """

    def __init__(self, base_url, organization_name, headers):
        super(TFEOrganizations,self).__init__(base_url, organization_name, headers)
        self._org_base_url = "{base_url}/organizations".format(base_url = base_url)

    def lst(self):
        """
        GET /organizations
        """
        return self._ls(self._org_base_url)

    def show(self, organization_name):
        """
        GET /organizations/:organization_name
        """
        url = "{0}/{1}".format(self._org_base_url,organization_name)
        return self._show(url)

