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
import tempfile


class PlanGenerator:

    def __init__(self, context, steps, delta):
        self.context = context
        self.steps = steps
        self.delta = delta

    def _is_create(self):
        return not self.delta.operation == Operation.DESTROY

    def _is_destroy(self):
        return not self._is_create()

    def generate(self):
        print(self.delta)
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
                          'organization': container.organization,
                          'provider': container,
                          'work_dir': work_dir,
                          'deployed_application': deployedApplication}

        for module in deployed.embeddedModules:
            self.context.addStep(self.steps.upload(
                description="Upload a module content {0} for {1}/{2}".format(module.name, organization.name, workspace),
                order=60,
                target_path="{0}/{1}".format(work_dir, module.name),
                create_target_path=True,
                target_host=deployed.container.organization.host,
                artifact=module
            ))

        for module in deployed.modules:
            jython_context['deployed'] = module
            is_embedded_module = len([em.name for em in deployed.embeddedModules if module.source == em.name]) > 0

            self.context.addStep(self.steps.template(
                description="Generate a module instance {0} for {1}/{2}".format(module.name, organization.name,
                                                                                workspace),
                order=60,
                target_path="{0}/{1}.tf".format(work_dir, module.name),
                template_path="xldtfe/templates/module.tf.ftl",
                create_target_path=True,
                target_host=deployed.container.organization.host,
                freemarker_context={"deployed": module,
                                    "generate_output_variables": self._is_create(),
                                    "is_embedded_module": is_embedded_module}
            ))

        self.context.addStep(self.steps.jython(
            description="Create or Get the Workspace {0}/{1}".format(
                workspace,
                container.organization.name),
            order=60,
            script="xldtfe/create_workspace.py",
            jython_context=jython_context
        ))

        self.context.addStep(self.steps.jython(
            description="Upload globale configuration version for {0} in {1}/{2}".format(
                deployed.name,
                organization.name,
                workspace),
            order=60,
            script="xldtfe/create_globale_configuration_version.py",
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
            self.context.addStep(self.steps.jython(
                description="Trigger the run of DESTROY plan for {0} on {1}/{2}".format(
                    deployed.name,
                    organization.name,
                    workspace),
                order=65,
                script="xldtfe/trigger_destroy.py",
                jython_context=jython_context
            ))
        else:
            self.context.addStep(self.steps.jython(
                description="Trigger the run of plan for {0} on {1}/{2}".format(
                    deployed.name,
                    organization.name,
                    workspace),
                order=65,
                script="xldtfe/trigger_run.py",
                jython_context=jython_context
            ))

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
