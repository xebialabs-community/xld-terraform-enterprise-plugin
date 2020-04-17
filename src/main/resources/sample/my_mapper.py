#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from terraform.mapper.resource_mapper import ResourceMapper


class AWSEC2Mapper(ResourceMapper):
    def __init__(self):
        super(AWSEC2Mapper, self).__init__(["overthere.SshHost"])
        self.attributes = {}

    def accepted_type(self):
        return 'aws_instance'

    def create_ci(self, tf_resource, folder, deployed):
        print("-- tf_resource['type'] {0}".format(tf_resource['type']))
        if not self.types_supported(tf_resource['type']):
            return None

        self.attributes = tf_resource['attributes']
        print("Creating CI of type 'overthere.SshHost")
        host_id = "{0}/{1}".format(folder, self.attributes['tags']['Name'])
        print(host_id)
        host_properties = {
            'os': 'UNIX',
            'address': self.attributes['public_ip'],
            'username': 'ubuntu',
            'privateKeyFile': deployed.mapperContext['privateKeyFile']
        }
        return [
            super(AWSEC2Mapper, self)._create_ci("overthere.SshHost", host_id, host_properties),
        ]
