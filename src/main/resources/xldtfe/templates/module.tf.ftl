<#--

    Copyright 2020 XEBIALABS

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

-->
module "${deployed.name}" {
<#if is_embedded_module>
    source = "./${deployed.source}"
<#else>
    source = "${deployed.source}"
</#if>

<#if deployed.version??>
    version = "${deployed.version}"
</#if>

<#list inputVariables?keys as key>
<#assign value=inputVariables[key]/>
    ${key} = ${value}

</#list>

<#list hcl_variables?keys as key>
    ${key} = ${hcl_variables[key]}
</#list>


<#list secretInputVariables?keys as key>
    ${key} = ${secretInputVariables[key]}
</#list>

}

<#if generate_output_variables>
    <#list outputVariables?keys as key>
output "${deployed.name}-${key}" {
  value = module.${deployed.name}.${outputVariables[key]}
}
    </#list>


    <#list secretOutputVariables?keys as key>
output "${deployed.name}-${key}" {
  value = module.${deployed.name}.${secretOutputVariables[key]}
  sensitive = true
}
    </#list>
</#if>

