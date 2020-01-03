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
Module for Terraform Enterprise API Endpoint: Variables.
"""

from .endpoint import TFEEndpoint

class TFEVariables(TFEEndpoint):
    """
    This set of APIs covers create, update, list and delete operations on variables.

    https://www.terraform.io/docs/enterprise/api/variables.html
    """
    def __init__(self, base_url, organization_name, headers, proxy_server):
        super(TFEVariables,self).__init__(base_url, organization_name, headers, proxy_server)
        self._base_url = "{base_url}/vars".format(base_url=base_url)

    def create(self, workspace_id,key,value, category, sensitive):
        """
        POST /vars
        """
        payload={ "data": { "type":"vars",
            "attributes": {
                "key":key,
                "value":value,
                "category":category,
                "hcl":"false",
                "sensitive":sensitive
                },
            "relationships": {
                "workspace": {
                    "data": {
                        "id":workspace_id,
                        "type":"workspaces"
                        }
                    }
                }
            }
            }
        return self._create(self._base_url, payload)

    def lst(self, workspace_name=None):
        """
        GET /vars
        """
        url = "{0}?filter[organization][name]={1}".format(self._base_url, self._organization_name)

        if workspace_name is not None:
            url += "&filter[workspace][name]={workspace_name}".format(workspace_name=workspace_name)

        return self._ls(url)

    def update(self, variable_id, payload):
        """
        PATCH /vars/:variable_id
        """
        url = "{0}/{1}".format(self._base_url,variable_id)
        return self._update(url, payload)

    def destroy(self, variable_id):
        """
        DELETE /vars/:variable_id
        """
        url = "{0}/{1}".format(self._base_url,variable_id)
        return self._destroy(url)
