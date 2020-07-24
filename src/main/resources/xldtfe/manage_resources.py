#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


from terraform.capture_output import capture_output
import com.xebialabs.overthere.CmdLine as CmdLine
import json

from com.xebialabs.deployit.provision import ProvisionHelper
from com.xebialabs.deployit.plugin.api.reflect import DescriptorRegistry
from com.xebialabs.deployit.plugin.api.reflect import Type
import importlib


class MapperFactory(object):
    @staticmethod
    def default_mappers():
        descriptor = DescriptorRegistry.getDescriptor('terraformEnterprise', 'Mappers')
        mapper_fqns = [p.getDefaultValue() for p in descriptor.getPropertyDescriptors() if p.name.endswith('_mapper')]
        mappers = [MapperFactory.new_mapper_instance(m) for m in mapper_fqns]
        return mappers

    @staticmethod
    def mappers(dict_of_mappers):
        mappers = [MapperFactory.new_mapper_instance(m) for m in dict_of_mappers.values()]
        return mappers

    @staticmethod
    def new_mapper_instance(full_class_string):
        print("new_mapper_instance: {0}".format(full_class_string))
        class_data = full_class_string.split(".")
        module_path = ".".join(class_data[:-1])
        class_str = class_data[-1]
        print(".import_module {0}".format(module_path))
        module = importlib.import_module(module_path)
        print(".reload {0}".format(module))
        reload(module)
        clazz = getattr(module, class_str)
        instance = clazz()
        return instance


class ManageResources(object):
    def __init__(self, task_context):
        self.repository = task_context['repositoryService']
        self.context = task_context['context']
        self.previousDeployed = task_context['previousDeployed']
        self.deployed = task_context['deployed']
        if self.deployed is None:
            self.current_deployed = self.previousDeployed
        else:
            self.current_deployed = self.deployed
        self.deployedApplication = task_context['deployedApplication']

        self.environment_id = ProvisionHelper.getProvisionEnvironmentId(
            self.current_deployed.environmentPath, self.deployedApplication.environment.id)
        self.environment = ProvisionHelper.getOrCreateEnvironment(
            self.environment_id, self.context)

        self.folder = "Infrastructure"
        self.generated_ids = []
        self.generated_cis = []
        self.cis_to_delete = []
        self.resource_mappers = MapperFactory.default_mappers()
        self.resource_mappers.extend(MapperFactory.mappers(self.current_deployed.container.additionalMappers))

    def process(self, output):
        self.process_resources(output)
        self.process_cis_to_delete()
        self.update_environment_members()
        self.update_generated_cis()
        self.delete_removed_resources()

    def process_resources(self, output):
        if not output:
            context.logOutput(
                "No resources found for '%s', skipping Infrastructure creation." % self.current_deployed.name)
            return

        output_json = output
        resources = []
        if 'modules' in output_json:
            for module in output_json['modules']:
                if 'resources' in module:
                    for resourceKey in module['resources']:
                        resource = module['resources'][resourceKey]
                        resources.append(resource)
        elif 'resources' in output_json:
            for resource in output_json['resources']:
                for instance in resource['instances']:
                    instance['type'] = resource['type']
                    resources.append(instance)

        for mapper in self.resource_mappers:
            candidates = [resource for resource in resources if resource['type'] in mapper.accepted_types()]
            if len(candidates) > 0:
                print("call {0} mapper managing {1} type(s) with {2} resource(s))".format(mapper, mapper.accepted_types(), len(candidates)))
                cis = mapper.create_ci(candidates, self.folder, self.deployed)
                print("{0} configuration item(s) to create or update".format(len(cis)))
                self.process_cis(cis)

    def process_cis(self, cis):
        for ci in cis:
            if ci is not None:
                if self.repository.exists(ci.id):
                    self.repository.update(ci.id, ci)
                    print("'%s' of type '%s' updated." % (ci.id, ci.type))
                else:
                    self.repository.create(ci.id, ci)
                    print("'%s' of type '%s' created." % (ci.id, ci.type))
                self.generated_cis.append(ci)
                self.generated_ids.append(ci.id)

    def process_cis_to_delete(self):
        if self.previousDeployed:
            for ci in self.previousDeployed.getProperty(self._get_managed_ci_property()):
                if ci.type != "udm.Environment" and ci.type != "udm.Dictionary":
                    if ci.id not in self.generated_ids:
                        self.cis_to_delete.append(ci.id)

    def update_environment_members(self):
        print("update_environment_members {0}".format(self.environment_id))
        environment = ProvisionHelper.getOrCreateEnvironment(self.environment_id, self.context)
        members = environment.members
        for ci in self.generated_cis:
            print("...generated ci {0}".format(ci.id))
            if 'Environments/' not in ci.id:
                print("...{0} added to 'members' property of environment '{1}'".format(ci.id, self.environment_id))
                members.add(ci)

        members_to_remove = []
        for ci in members:
            if ci.id in self.cis_to_delete:
                print("'%s' removed from 'members' property of environment '%s'" %
                      (ci.id, self.environment_id))
                members_to_remove.append(ci)
        for ci in members_to_remove:
            members.remove(ci)
        environment.setMembers(members)
        print(".members {0}".format(members))
        self.repository.update(self.environment_id, environment)

    def update_generated_cis(self):
        generated_configuration_items = self.current_deployed.getProperty(self._get_managed_ci_property())

        for ci in self.generated_cis:
            generated_configuration_items.add(ci)
        if self.environment_id != self.deployedApplication.environment.id:
            generated_configuration_items.add(self.repository.read(self.environment_id))

        generated_to_remove = []
        for ci in generated_configuration_items:
            if ci.id in self.cis_to_delete:
                print("'%s' removed from 'generated_configuration_items' property of '%s'" % (ci.id, self.current_deployed.id))
                generated_to_remove.append(ci)
        for ci in generated_to_remove:
            generated_configuration_items.remove(ci)

        self.current_deployed.setProperty(self._get_managed_ci_property(), generated_configuration_items)

        if self.repository.exists(self.current_deployed.id):
            self.repository.update(self.current_deployed.id, self.current_deployed)

    def delete_removed_resources(self):
        for ci_id in self.cis_to_delete:
            self.repository.delete(ci_id)
            print("'%s' deleted" % ci_id)

    def _get_managed_ci_property(self):
        # Why do we need to manage this indirection to the list of managed_ci ?
        # Because the DeleteAllProvisionedItems steps assumes the generatedConfigurationItems property is managed
        # only if the type is base of udm.BaseDeployedInfrastructureAsCode else it filters out the ci.
        # so depending of the type of the subclass the code uses generatedConfigurationItems or boundConfigurationItems
        if self._is_sub_of_based_deployed_infructure_as_code():
            # print(" ... _get_managed_ci_property:generatedConfigurationItems")
            return "generatedConfigurationItems"
        else:
            # print(" ... _get_managed_ci_property:boundConfigurationItems")
            return "boundConfigurationItems"

    def _is_sub_of_based_deployed_infructure_as_code(self):
        current_deployed_type = self.current_deployed.getType()
        bdiac_type = Type.valueOf('udm.BaseDeployedInfrastructureAsCode')
        return current_deployed_type.isSubTypeOf(bdiac_type)


from terraxld.api import TFE

import sys
import json
import tempfile

myapi = TFE(organization)
ws_id = myapi.workspaces.get_id(workspace_name)
output = myapi.state_versions.get_current_state_content_workspace(ws_id)

if debug:
    print("---- output")
    outfile = tempfile.NamedTemporaryFile(delete=False, prefix="xld-tfe-", suffix="-output.json")
    print("dump output to {0}".format(outfile.name))
    json.dump(output, outfile, indent=4)
    print(50 * '-')
    json.dump(output, sys.stdout, indent=4)
    print(50 * '-')
    outfile.close()
    print("---- /output")

ManageResources(locals()).process(output)
