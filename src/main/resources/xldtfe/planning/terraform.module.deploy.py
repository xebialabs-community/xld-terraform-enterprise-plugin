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

        provider = deployed.container
        organization = deployed.container.workspace.organization
        workspace = deployed.container.workspace

        work_dir = tempfile.mkdtemp()
        print("work_directory:{0}".format(work_dir))

        jython_context = {
            'terraform_version': workspace.terraformVersion,
            'workspace': workspace,
            'organization': organization,
            'provider': provider,
            'work_dir': work_dir,
            'deployed': deployed}

        if self._is_create():
            self.context.addStep(self.steps.jython(
                description="Capture output variables for {0} for {1}".format(deployed.name, self.to_desc(provider)),
                order=66,
                script="xldtfe/capture_output_variables.py",
                jython_context=jython_context
            ))

        self.context.addStep(self.steps.jython(
            description="Check the {0} Workspace exists".format(self.to_desc(provider)),
            order=60,
            script="xldtfe/check_workspace.py",
            jython_context=jython_context
        ))

        self.context.addStep(self.steps.jython(
            description="Upload module configuration version for {0} in {1}".format(
                deployed.name,
                self.to_desc(provider)),
            order=60,
            script="xldtfe/create_configuration_version.py",
            jython_context=jython_context
        ))

        self.context.addStep(self.steps.wait(
            description="Wait for the load of the configuration",
            order=60,
            seconds=5
        ))

        self.context.addStep(self.steps.jython(
            description="Set the variables for {0}".format(self.to_desc(provider)),
            order=60,
            script="xldtfe/set_variables.py",
            jython_context=jython_context
        ))

        self.context.addStep(self.steps.jython(
            description="Set the environment for {0}".format(self.to_desc(provider)),
            order=60,
            script="xldtfe/set_environment.py",
            jython_context=jython_context
        ))

        if self._is_destroy():
            self.context.addStep(self.steps.jython(
                description="Trigger the run of DESTROY plan for {0} on {1}".format(
                    deployed.name,
                    self.to_desc(provider)),
                order=65,
                script="xldtfe/trigger_destroy.py",
                jython_context=jython_context
            ))
        else:
            self.context.addStep(self.steps.jython(
                description="Trigger the run of plan for {0} on {1}".format(
                    deployed.name,
                    self.to_desc(provider)),
                order=65,
                script="xldtfe/trigger_run.py",
                jython_context=jython_context
            ))

        self.context.addStep(self.steps.jython(
            description="Wait for the end of the execution of the plan {0} on {1}".format(
                deployed.name,
                self.to_desc(provider)),
            order=65,
            script="xldtfe/wait_for_run.py",
            jython_context=jython_context
        ))

    def to_desc(self, provider):
        return "{0}/{1}[{2}]".format(provider.workspace.organization.name, provider.workspace.name, provider.name)


PlanGenerator(context, steps, delta).generate()
