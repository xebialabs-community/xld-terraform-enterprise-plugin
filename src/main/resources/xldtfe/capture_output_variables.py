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
import re
import json


def dump_json(data, message):
    if True:
        print(50 * '=')
        print(message)
        print(50 * '=')
        json.dump(data, sys.stdout, indent=4)
        print(50 * '=')


myapi = TFE(organization)
ws_id = myapi.workspaces.get_id(workspace_name)
output = myapi.state_versions.get_current_state_content_workspace(ws_id)
# dump_json(output,"OUTPUT")


if output:
    output_variables = {}
    output_json = output['outputs']

    for key in output_json:
        var_type = output_json[key]['type']
        print("{0}:{1}/{2}".format(key, var_type, type(var_type)))
        if isinstance(var_type, list):
            for num, value in enumerate(output_json[key]['value']):
                idx_key = "{0}_{1}".format(key, num)
                print("   add {0}={1}".format(idx_key, value))
                output_variables[idx_key] = value
        else:
            print("   add {0}={1}".format(key, output_json[key]['value']))
            output_variables[key] = output_json[key]['value']
            print("new output variable found {0}:{1}".format(key, output_variables[key]))
            expression_reg_exp = re.compile("([a-zA-Z_1-9]*)-([a-zA-Z_1-9]*)")
            mo = expression_reg_exp.findall(key)
            if len(mo) == 1:
                module = mo[0][0]
                output_var = mo[0][1]
                print("{0} => {1}".format(module, output_var))
                instantiated_module = [ci for ci in deployed.modules if ci.id.endswith(module)][0]
                print("instantiated module {0}".format(instantiated_module))
                if deployed.removeModulePrefixNameInDictionary:
                    print("   add {0}={1}".format(output_var, output_json[key]['value']))
                    output_variables[output_var] = output_json[key]['value']
                if instantiated_module.hasProperty(output_var):
                    instantiated_module.setProperty(output_var, output_json[key]['value'])
                else:
                    print("{0} hasn't {1} property, can't assign the value to the CI".format(instantiated_module, output_var))

    deployed.outputVariables = output_variables
    context.logOutput("Output variables from Terraform captured.")
    context.logOutput("---- outputVariables -----")
    for k,v in sorted(deployed.outputVariables.items()):
        print("-> {0}={1}".format(k, v))
    context.logOutput("---- /outputVariables -----")

else:
    context.logOutput("No output variables found.")



