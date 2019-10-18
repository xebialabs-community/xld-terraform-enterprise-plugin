"""
Module for Terraform Enterprise API Endpoint: Variables.
"""

from .endpoint import TFEEndpoint

class TFEVariables(TFEEndpoint):
    """
    This set of APIs covers create, update, list and delete operations on variables.

    https://www.terraform.io/docs/enterprise/api/variables.html
    """
    def __init__(self, base_url, organization_name, headers):
        super(TFEVariables,self).__init__(base_url, organization_name, headers)
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
