#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys

import com.xebialabs.deployit.plugin.api.reflect.Type as Type


class ManageDictionaryStep:

    def __init__(self, deployed, deployed_application, repository_service, context):
        self.deployed = deployed
        self.deployed_application = deployed_application
        self.environment_id = self.deployed_application.environment.id
        self.repository_service = repository_service
        self.context = context

    def fill(self):
        dictionary = self._get_dictionary()
        self.context.logOutput(dictionary.id)
        new_entries = {}
        for k, v in self.deployed.outputVariables.items():
            self.context.logOutput("...add {0}:{1} to the dictionary".format(k, v))
            new_entries[k] = v
        dictionary.entries = new_entries
        self.repository_service.update([dictionary])
        self.context.logOutput("Dictionary filled: '{0}'".format(dictionary))

        environment = self.repository_service.read(self.environment_id)
        if dictionary not in environment.dictionaries:
            list_of_dict = environment.dictionaries
            list_of_dict.append(dictionary)
            environment.dictionaries = list_of_dict
            self.repository_service.update([environment])
            self.context.logOutput("Dictionary added to Environment '{0}'".format(environment.id))
            current_bound_configuration_items = self.deployed.boundConfigurationItems
            current_bound_configuration_items.add(dictionary)
            deployed.boundConfigurationItems = current_bound_configuration_items

    def delete(self):
        dictionary_id = self._get_dictionary_id()
        environment = self.repository_service.read(self.environment_id)
        list_of_dict = [d for d in environment.dictionaries if not d.id == dictionary_id]
        environment.dictionaries = list_of_dict
        self.repository_service.update([environment])
        self.context.logOutput("Dictionary removed from Environment '{0}'".format(environment.id))
        self.repository_service.delete(dictionary_id)
        self.context.logOutput("Dictionary removed '{0}'".format(dictionary_id))

    def _get_dictionary_id(self):
        if self.deployed.dictionaryPath is None:
            return "{0}/{1}-dictionary".format('/'.join(self.environment_id.split('/')[:-1]), self.deployed.name)
        else:
            if self.deployed.dictionaryPath.startswith('Environments/'):
                return self.deployed.dictionaryPath
            else:
                return "{0}/{1}".format('/'.join(self.environment_id.split('/')[:-1]), self.dictionaryPath)

    def _get_dictionary(self):
        dictionary_id = self._get_dictionary_id()
        self.context.logOutput(dictionary_id)
        if self.repository_service.exists(dictionary_id):
            self.context.logOutput("get dictionary {0}".format(dictionary_id))
            return self.repository_service.read(dictionary_id)
        else:
            self._create_directories(dictionary_id)
            type = Type.valueOf('udm.Dictionary')
            configuration_item = type.descriptor.newInstance(dictionary_id)
            self.context.logOutput("create new dictionary {0}".format(configuration_item))
            self.repository_service.create([configuration_item])
            return self.repository_service.read(dictionary_id)

    def _create_directories(self, ci_id):
        self.context.logOutput("_create_directories for {0}".format(ci_id))
        full_path_id = []
        for ci in ci_id.split('/')[:-1]:
            full_path_id.append(ci)
            current_id = "/".join(full_path_id)
            self.context.logOutput("test {0}".format(current_id))
            if self.repository_service.exists(current_id):
                read_ci = self.repository_service.read(current_id)
                if read_ci.type not in ['internal.Root', 'core.Directory']:
                    raise Exception(
                        "'{0}' is invalid. '{1}' must be a directory under 'Environments'.".format(current_id, ci_id))
            else:
                type = Type.valueOf('core.Directory')
                configuration_item = type.descriptor.newInstance(current_id)
                self.context.logOutput("create new directory {0}".format(configuration_item))
                self.repository_service.create([configuration_item])


step = ManageDictionaryStep(deployed=deployed,
                            deployed_application=deployed_application,
                            repository_service=repositoryService,
                            context=context)
getattr(step, operation)()


