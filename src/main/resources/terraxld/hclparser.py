#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import tempfile
import os

import hcl


class HclParser:

    def __init__(self, recurse_directory=False):
        self._load_dat_file()
        self.variable = dict()
        self.output = dict()
        self.recurse_directory = recurse_directory
        pass

    def _load_dat_file(self):
        hcl.parser.pickle_file = self._load_classpath_resource('parsetab.dat')
        # print("_load_dat_file: {0}".format(hcl.parser.pickle_file))

    def parse_file(self, file):
        fp = open(file, 'rb')
        try:
            return hcl.load(fp)
        except ValueError as ve:
            print("error when parsing {0}: {1}, skip it".format(file, ve))
            # import traceback
            # print(str(traceback.format_exc()))
            return dict()
        except:
            print("error when parsing {0}, skip it".format(file))
            # import traceback
            # print(str(traceback.format_exc()))
            return dict()
        finally:
            fp.close()

    def parse_folder(self, overthere_folder):
        print("parse_folder {0}".format(overthere_folder.getPath()))
        for f in overthere_folder.listFiles():
            if f.isDirectory():
                if self.recurse_directory:
                    self.parse_folder(f)
                else:
                    continue
            else:
                data = self.parse_file(f.getFile().getPath())
                # print(data)
                if 'variable' in data:
                    self.variable.update(data['variable'])
                if 'output' in data:
                    self.output.update(data['output'])

    def parse_deployed(self, deployed):
        self.parse_folder(overthere_folder=deployed.file)

    def is_hcl_variable(self, variable_name):
        # print "?is_hcl_variable {0}".format(variable_name)
        if variable_name in self.variable:
            variable_data = self.variable[variable_name]
            return self._is_hcl_variable(variable_data)
        return False

    def _is_hcl_variable(self, variable_data):
        # print "??_is_hcl_variable {0}?".format(variable_data)
        if 'type' in variable_data:
            if 'bool' in variable_data['type']:
                return False
            elif 'map' in variable_data['type']:
                return True
            elif 'list' in variable_data['type']:
                return True
            elif 'string' in variable_data['type']:
                return False
            else:
                return True
        else:
            return False

    def _load_classpath_resource(self, resource):
        from java.lang import Thread
        from com.google.common.io import Resources
        from java.io import File, FileOutputStream

        fobj = tempfile.NamedTemporaryFile()

        url = Thread.currentThread().contextClassLoader.getResource(resource)
        if url is None:
            raise Exception("Resource [%s] not found on classpath." % resource)

        fop = FileOutputStream(File(fobj.name));
        Resources.copy(url, fop)
        fop.close()
        return fobj.name
