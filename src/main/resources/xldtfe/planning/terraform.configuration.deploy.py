#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from com.xebialabs.deployit.plugin.api.deployment.specification import Operation
from com.xebialabs.deployit.plugin.api.reflect import PropertyKind
import tempfile
import json
import re


class PlanGenerator:

    def __init__(self, context, steps, delta):
        self.context = context
        self.steps = steps
        self.delta = delta

    def _is_create(self):
        return not self.delta.operation == Operation.DESTROY

    def _is_destroy(self):
        return not self._is_create()

    def _extract_entry(self, map_variables, k):
        for map_var in map_variables:
            if k == map_var.name:
                map = dict(map_var.variables)
                for pd in map_var.type.descriptor.propertyDescriptors:
                    if pd.category in "Input" and pd.kind.isSimple():
                        map[pd.name] = map_var.getProperty(pd.name)
                return map
        raise Exception("{0} not found in {1}".format(k, map_variables))

    def _process_map_variables(self, module):
        map_variables = module.mapInputVariables

        regexp = module.mapArrayRegexp
        # return a map map_variable.name => map_variables.variables
        # merge the entries that follows this patern
        # [xxxx__0,xxxx__1,xxx__2] =>'xxxx'=>[(...),(...),(...)]
        temporary_map = {}
        expression_reg_exp = re.compile(regexp)

        map_of_ci = {}
        for var in map_variables:
            map_of_ci[var.name]=var

        all_keys = list(map_of_ci.keys())
        all_keys.sort()

        for k in all_keys:
            mo = expression_reg_exp.findall(k)
            if len(mo) == 0:
                temporary_map[k] = self._extract_entry(map_variables, k)
            else:
                key = mo[0][0]
                if map_of_ci[k].useTfVariableName:
                    key=map_of_ci[k].tfVariableName

                number = int(mo[0][1]) - 1
                if key not in temporary_map:
                    temporary_map[key] = []
                temporary_map[key].insert(number, self._extract_entry(map_variables, k))

        return temporary_map

    def _compute_properties(self, deployed):
        properties = {'inputVariables': {},
                      'secretInputVariables': deployed.secretInputVariables,
                      'outputVariables': deployed.outputVariables,
                      'secretOutputVariables': deployed.secretOutputVariables,
                      'inputHCLVariables': {}}

        for key, value in deployed.inputVariables.items():
            print("inputVariables process {}->{}".format(key, value))
            if value.startswith(deployed.dependencyAnnotation):
                value = "module.{0}.{1}".format(value[2:], key)
            else:
                value = json.dumps(value)
            properties['inputVariables'][key] = value

        for key, value in deployed.inputHCLVariables.items():
            print("inputHCLVariables process {}->{}".format(key, value))
            if value.startswith(deployed.dependencyAnnotation):
                value = "module.{0}.{1}".format(value[2:], key)
            else:
                value = value
            properties['inputVariables'][key] = value

        for pd in deployed.type.descriptor.propertyDescriptors:
            if pd.category in deployed.inputCategory:
                if pd.kind.isSimple():
                    if pd.isPassword():
                        properties['secretInputVariables'][pd.name] = json.dumps(deployed.getProperty(pd.name))
                    else:
                        value = deployed.getProperty(pd.name)
                        if pd.kind == PropertyKind.STRING:
                            value = json.dumps(self.__translate_dependency_annotation(deployed, pd.name, value))
                        else:
                            value = json.dumps(value)
                        properties['inputVariables'][pd.name] = value
                elif pd.kind == PropertyKind.MAP_STRING_STRING:
                    properties['inputVariables'][pd.name] = json.dumps(deployed.getProperty(pd.name))
                elif pd.kind == PropertyKind.LIST_OF_STRING or pd.kind == PropertyKind.SET_OF_STRING:
                    values = [self.__translate_dependency_annotation(deployed, pd.name, value, True) for value in deployed.getProperty(pd.name)]
                    properties['inputVariables'][pd.name] = json.dumps(values)

            if pd.category in deployed.outputCategory:
                if pd.kind.isSimple() and pd.isPassword():
                    properties['secretOutputVariables'][pd.name] = pd.name
                else:
                    properties['outputVariables'][pd.name] = pd.name

        return properties

    def __translate_dependency_annotation(self, deployed, name, value, interpolate=False):
        if value.startswith(deployed.dependencyAnnotation):
            new_value = "module.{0}.{1}".format(value[2:], name)
            if interpolate:
                return "${" + new_value + "}"
            return new_value
        else:
            return value

    def _map_to_json(self, data):
        new_data = {}
        for key, value in data.iteritems():
            new_data[str(key)] = json.dumps(value)
        return new_data

    def generate(self):
        if self._is_destroy():
            deployed = self.delta.previous
        else:
            deployed = self.delta.deployed

        container = deployed.container
        organization = container.organization
        workspace = deployed.workspaceName

        work_dir = tempfile.mkdtemp()
        print("work_directory:{0}".format(work_dir))

        jython_context = {'workspace_name': workspace,
                          'terraform_version': deployed.terraformVersion,
                          'organization': organization,
                          'provider': container,
                          'work_dir': work_dir,
                          'deployed_application': deployedApplication}

        for module in deployed.embeddedModules:
            self.context.addStep(self.steps.upload(
                description="Upload a module content {0} for {1}/{2}".format(module.name, organization.name, workspace),
                order=60,
                target_path="{0}/{1}".format(work_dir, module.name),
                create_target_path=True,
                target_host=organization.host,
                artifact=module
            ))

        for module in deployed.modules:
            jython_context['deployed'] = module

            is_embedded_module = len([em.name for em in deployed.embeddedModules if module.source == em.name]) > 0
            hcl_variables = self._process_map_variables(module)
            hcl_variables = self._map_to_json(hcl_variables)

            freemarker_context = self._compute_properties(module)

            freemarker_context.update({"deployed": module,
                                       "generate_output_variables": self._is_create(),
                                       "is_embedded_module": is_embedded_module,
                                       "hcl_variables": hcl_variables})

            self.context.addStep(self.steps.template(
                description="Generate a module instance {0} for {1}/{2}".format(module.name, organization.name, workspace),
                order=60,
                target_path="{0}/{1}.tf".format(work_dir, module.name),
                template_path="xldtfe/templates/module.tf.ftl",
                create_target_path=True,
                target_host=organization.host,
                freemarker_context=freemarker_context
            ))

        self.context.addStep(self.steps.jython(
            description="Create or Get the Workspace {0}/{1}".format(
                workspace,
                organization.name),
            order=60,
            script="xldtfe/create_workspace.py",
            jython_context=jython_context
        ))

        self.context.addStep(self.steps.jython(
            description="Upload global configuration version for {0} in {1}/{2}".format(
                deployed.name,
                organization.name,
                workspace),
            order=60,
            script="xldtfe/create_global_configuration_version.py",
            jython_context=jython_context
        ))

        self.context.addStep(self.steps.wait(
            description="Wait for the load of the configuration",
            order=60,
            seconds=5
        ))

        self.context.addStep(self.steps.jython(
            description="Set the environment {0} in {1}/{2}".format(
                container.name,
                organization.name,
                workspace),
            order=60,
            script="xldtfe/set_environment.py",
            jython_context=jython_context
        ))

        if self._is_destroy():
            self.context.addStepWithCheckpoint(self.steps.jython(
                description="Trigger the run of DESTROY plan for {0} on {1}/{2}".format(
                    deployed.name,
                    organization.name,
                    workspace),
                order=65,
                script="xldtfe/trigger_destroy.py",
                jython_context=jython_context
            ), self.delta)
        else:
            self.context.addStepWithCheckpoint(self.steps.jython(
                description="Trigger the run of plan for {0} on {1}/{2}".format(
                    deployed.name,
                    organization.name,
                    workspace),
                order=65,
                script="xldtfe/trigger_run.py",
                jython_context=jython_context
            ), self.delta)

        self.context.addStep(self.steps.jython(
            description="Wait for the end of the execution of the plan {0} on {1}/{2}".format(
                deployed.name,
                organization.name,
                workspace),
            order=65,
            script="xldtfe/wait_for_run.py",
            jython_context=jython_context
        ))

        if self._is_create():
            jython_context['deployed'] = deployed
            self.context.addStep(self.steps.jython(
                description="Capture output variables for {0} for {1}/{2}".format(deployed.name, organization.name,
                                                                                  workspace),
                order=66,
                script="xldtfe/capture_output_variables.py",
                jython_context=jython_context
            ))

        if self._is_create() and deployed.automaticDictionary:
            jython_context['deployed'] = deployed
            jython_context['operation'] = 'fill'
            self.context.addStep(self.steps.jython(
                description="Fill Dictionary with captured output variables for '{0}' for {1}/{2}".format(deployed.name,
                                                                                                          organization.name,
                                                                                                          workspace),
                order=90,
                script="xldtfe/manage_dictionary.py",
                jython_context=jython_context
            ))
        else:
            jython_context['deployed'] = deployed
            jython_context['operation'] = 'delete'
            jython_context['deployed_application'] = previousDeployedApplication
            self.context.addStep(self.steps.jython(
                description="Delete Dictionary associated for '{0}' for {1}/{2}".format(deployed.name,
                                                                                        organization.name,
                                                                                        workspace),
                order=90,
                script="xldtfe/manage_dictionary.py",
                jython_context=jython_context
            ))


PlanGenerator(context, steps, delta).generate()
