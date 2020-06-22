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

import os
import stat
import os.path


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
        # deployed.mapperContext['key_pair-private_key_pem']
        if 'XLD_TAGS' in self.attributes['tags']:
            tags = set(self.attributes['tags']['XLD_TAGS'].split(','))
        else:
            tags = set("")

        host_properties = {
            'os': 'UNIX',
            'address': self.attributes['public_ip'],
            'username': 'ubuntu',
            'sudoUsername': 'root',
            'privateKeyFile': self._store_private_key('./ssh-key/{0}.pem'.format(self.attributes['tags']['Name']), deployed.outputVariables['key_pair-private_key_pem']),
            'tags': tags
        }
        print(host_properties)
        return [
            super(AWSEC2Mapper, self)._create_ci("overthere.SshHost", host_id, host_properties),
        ]

    def _store_private_key(self, pem_file_path, key_material):
        print(pem_file_path)
        if len(pem_file_path) > 0:
            self._delete_pem_file(pem_file_path)
            print("store the key in {0}".format(pem_file_path))
            directory = os.path.abspath(os.path.join(pem_file_path, os.pardir))
            if not os.path.isdir(directory):
                print("create Parent Directory: {0}".format(directory))
                os.makedirs(directory)

            with open(pem_file_path, "w") as text_file:
                text_file.write(key_material)
            print("set the key read only {0}".format(pem_file_path))
            os.chmod(pem_file_path, stat.S_IRUSR)
        return pem_file_path

    def _delete_pem_file(self, pem_file_path):
        if os.path.isfile(pem_file_path):
            print("unset the key read only {0}".format(pem_file_path))
            os.chmod(pem_file_path, stat.S_IRUSR | stat.S_IWUSR)
            print("remove pem file {0}".format(pem_file_path))
            os.remove(pem_file_path)
