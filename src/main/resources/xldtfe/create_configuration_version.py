#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from terraxld.api import TFE
import glob
import tarfile
import os
from com.xebialabs.overthere.local import LocalFile,LocalConnection

def tar_directory(source_dir):
    archive_file = LocalConnection.getLocalConnection().getTempFile("tfe-xld.tgz")
    print(archive_file)
    print(archive_file.path)

    tar = tarfile.open(archive_file.path, "w:gz")
    for file_name in glob.glob(os.path.join(source_dir, "*")):
        print("  Adding %s..." % file_name)
        tar.add(file_name, os.path.basename(file_name))
    tar.close()
    return archive_file


artifact=deployed.file.path
archive_file = tar_directory(artifact)
print("TGZ:"+archive_file.path)

myapi = TFE(organization)
ws_id = myapi.workspaces.get_id(workspace)
config_version=myapi.config_versions.create(ws_id)

if 'data' not in config_version:
    raise Exception("Cannot create a new config_version. Have you used an Organization API tokens instead of a User or Team token ? Organization API tokens are designed for creating and configuring workspaces and teams. {0}".format(config_version))

cv_id = config_version['data']['id']
print("New configuration version {0}".format(cv_id))

print("upload the tgz")
myapi.config_versions.upload(archive_file.path,cv_id)

context.setAttribute(ws_id + "_cv_id", cv_id)



