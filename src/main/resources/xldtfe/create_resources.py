#
# Copyright 2019 XEBIALABS
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
from terraform.mapper.gke_cluster_mapper import GKEClusterMapper
from terraform.mapper.aks_cluster_mapper import AKSClusterMapper
from com.xebialabs.deployit.provision import ProvisionHelper
from xldtfe.mapper.aws_s3_mapper import AWSS3Mapper

class CreateResources(object):
    def __init__(self, task_context):
        self.repository = task_context['repositoryService']
        self.context = task_context['context']
        self.previousDeployed = task_context['previousDeployed']
        self.deployed = task_context['deployed']
        self.deployedApplication = task_context['deployedApplication']
        self.environment_id = ProvisionHelper.getProvisionEnvironmentId(
            self.deployed.environmentPath, self.deployedApplication.environment.id)
        self.environment = ProvisionHelper.getOrCreateEnvironment(
            self.environment_id, context)

        self.folder = "Infrastructure"
        self.generated_ids = []
        self.generated_cis = []
        self.cis_to_delete = []
        self.resource_mappers = {
            'google_container_cluster': GKEClusterMapper(),
            'azurerm_kubernetes_cluster': AKSClusterMapper(),
            'aws_s3_bucket':  AWSS3Mapper()
        }

    def process(self, output):
        self.process_resources(output)
        self.process_cis_to_delete()
        self.update_environment_members()
        self.update_generated_cis()
        self.delete_removed_resources()

    def process_resources(self, output):       
        if output:
            output_json = output
            if 'modules' in output_json:
                for module in output_json['modules']:
                    if 'resources' in module:
                        for resourceKey in module['resources']:
                            resource = module['resources'][resourceKey]
                            self.process_resource(resource)
            elif 'resources' in output_json:
                for resource in output_json['resources']:
                    for instance in resource['instances']:
                        instance['type'] = resource['type']
                        self.process_resource(instance)
        else:
            context.logOutput(
                "No resources found for '%s', skipping Infrastructure creation." % deployed.name)

    def process_resource(self, resource):
        if resource['type'] in self.resource_mappers:
            cis = self.resource_mappers[resource['type']].create_ci(
                resource, self.folder,self.deployed)
            for ci in cis:
                if ci is not None:
                    if self.repository.exists(ci.id):
                        self.repository.update(ci.id, ci)
                        print("'%s' of type '%s' updated from '%s' resource." % (
                            ci.id, ci.type, resource['type']))
                    else:
                        self.repository.create(ci.id, ci)
                        print("'%s' of type '%s' created from '%s' resource." % (
                            ci.id, ci.type, resource['type']))
                    self.generated_cis.append(ci)
                    self.generated_ids.append(ci.id)
        else:
            context.logOutput(
                "Skipping '%s' as it is not a candidate for infrastructure creation." % resource['type'])

    def process_cis_to_delete(self):
        if (self.previousDeployed):
            for ci in self.previousDeployed.generatedConfigurationItems:
                if ci.type != "udm.Environment" and ci.type != "udm.Dictionary":
                    if ci.id not in self.generated_ids:
                        self.cis_to_delete.append(ci.id)

    def update_environment_members(self):
        print ("update_environment_members {0}".format(self.environment_id))
        
        environment = ProvisionHelper.getOrCreateEnvironment(
            self.environment_id, self.context)
        members = environment.members
        for ci in self.generated_cis:
            print("...generated ci {0}".format(ci.id))
            if 'Environments/' not in ci.id:
                print("...{0} added to 'members' property of environment '{1}'".format(ci.id,self.environment_id))
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
        generatedConfigurationItems = self.deployed.generatedConfigurationItems
        for ci in self.generated_cis:
            generatedConfigurationItems.add(ci)
        if self.environment_id != self.deployedApplication.environment.id:
            generatedConfigurationItems.add(
                self.repository.read(self.environment_id))

        generated_to_remove = []
        for ci in generatedConfigurationItems:
            if ci.id in self.cis_to_delete:
                print("'%s' removed from 'generatedConfigurationItems' property of '%s'" % (
                    ci.id, self.deployed.id))
                generated_to_remove.append(ci)
        for ci in generated_to_remove:
            generatedConfigurationItems.remove(ci)
        self.deployed.setGeneratedConfigurationItems(
            generatedConfigurationItems)
        if self.repository.exists(self.deployed.id):
            self.repository.update(self.deployed.id, self.deployed)

    def delete_removed_resources(self):
        for ci_id in self.cis_to_delete:
            self.repository.delete(ci_id)
            print("'%s' deleted" % ci_id)



from terraxld.api import TFE
import os
import sys
import json

organization = deployed.container.organization
myapi = TFE(api_token=organization.token, url=organization.url)
myapi.set_organization(organization.name)
workspace_name = deployed.workspaceName
ws_id = myapi.workspaces.get_id(workspace_name)

output = myapi.state_versions.get_current_state_content_workspace(ws_id)

CreateResources(locals()).process(output)
