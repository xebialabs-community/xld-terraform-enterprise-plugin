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

    def __init__(self, base_url, organization, headers):
        super(TFEOrganizations, self).__init__(base_url, organization, headers)
        self._org_base_url = "{base_url}/organizations".format(base_url=base_url)

    def lst(self):
        """
        GET /organizations
        """
        return self._ls(self._org_base_url)

    def show(self, organization_name):
        """
        GET /organizations/:organization_name
        """
        url = "{0}/{1}".format(self._org_base_url, organization_name)
        return self._show(url)
