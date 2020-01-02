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
Module containing class for common endpoint implementations across all TFE Endpoints.
"""

import json
import logging
import requests


class TFEEndpoint(object):
    """
    Base class providing common CRUD operation implementations across all TFE Endpoints.
    """

    def __init__(self, base_url, organization_name, headers, proxy_server):
        self._base_url = base_url
        self._headers = headers
        self._organization_name = organization_name
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)
        self._verify = False
        if proxy_server:
            proxy_url = "{}://{}:{}".format(str(proxy_server.protocol).lower(), proxy_server.hostname, proxy_server.port)
            self._proxies = {'http': proxy_url,'https': proxy_url}
            self._logger.debug("setup proxies {0}".format(proxy_url))
        else:
            self._proxies = None
 
        if self._verify == False:
            import urllib3
            urllib3.disable_warnings()


    def _create(self, url, payload):
        """
        Implementation the common create resource pattern for the TFE API.
        """
        results = None
        self._logger.debug(json.dumps(payload))
        req = requests.post(url, json.dumps(payload), headers=self._headers, verify=self._verify,  proxies=self._proxies)

        if req.status_code == 201:
            results = json.loads(req.content)
            return results
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)
            return err

    def _destroy(self, url):
        """
        Implementation of the common destroy resource pattern for the TFE API.
        """
        req = requests.delete(url, headers=self._headers, verify=self._verify, proxies=self._proxies)

        valid_status_codes = [200, 204]
        if req.status_code in valid_status_codes:
            self._logger.debug("Terraform Enterprise resource at URL [{url}] destroyed.".format(url=url))
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

    def _ls(self, url):
        """
        Implementation of the common list resources pattern for the TFE API.
        """
        results = None
        req = requests.get(url, headers=self._headers, verify=self._verify, proxies=self._proxies)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results


    def _show(self, url):
        """
        Implementation of the common show resource pattern for the TFE API.
        """
        results = None
        req = requests.get(url, headers=self._headers, verify=self._verify, proxies=self._proxies)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def _update(self, url, payload):
        """
        Implementation of the common update resource pattern for the TFE API.
        """
        req = requests.patch(url, data=json.dumps(payload), headers=self._headers, verify=self._verify, proxies=self._proxies)

        if req.status_code == 200:
            results = json.loads(req.content)
        else:
            err = json.loads(req.content.decode("utf-8"))
            self._logger.error(err)

        return results

    def _download(self, url):
        """
        Implementation of the common show resource pattern for the TFE API.
        """
        results = None
        self._logger.debug("_download {0}".format(url))
        req = requests.get(url, headers=self._headers, verify=self._verify, proxies=self._proxies)

        if req.status_code == 200:
            results = req.content
        else:
            err = req.content.decode("utf-8")
            self._logger.error(err)

        return results

    def _stream(self, url):
        """
        Stream the resource
        """
        results = None
        self._logger.debug("_stream {0}".format(url))
        req = requests.get(url, headers=self._headers, verify=self._verify, proxies=self._proxies,stream=True)
        return req

