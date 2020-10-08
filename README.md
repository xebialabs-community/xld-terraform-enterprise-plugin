# XL Deploy Terraform Enterprise Plugin

[![Build Status][xld-terraform-enterprise-plugin-travis-image]][xld-terraform-enterprise-plugin-travis-url]
[![License: MIT][xld-terraform-enterprise-plugin-license-image]][xld-terraform-enterprise-plugin-license-url]
![Github All Releases][xld-terraform-enterprise-plugin-downloads-image]

[xld-terraform-enterprise-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xld-terraform-enterprise-plugin.svg?branch=master
[xld-terraform-enterprise-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xld-terraform-enterprise-plugin
[xld-terraform-enterprise-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xld-terraform-enterprise-plugin-license-url]: https://opensource.org/licenses/MIT
[xld-terraform-enterprise-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-com]

## Preface

This document describes the functionality provided by the XL Deploy Terraform Enterprise plugin 

## Overview

## Installation

* requirement xl-deploy-server 9.0.0+
* Copy the latest JAR file from the [releases page](https://github.com/xebialabs-community/xld-helm-plugin/releases) into the `XL_DEPLOY_SERVER/plugins` directory.
* Restart the XL Deploy server.

## Sample Configuration
A sample configuration is available in the project.

store you azure credentials into ~/.xebialabs/azure.secrets.xlvals (you can use dummy values)
````
cat ~/.xebialabs/azure.secrets.xlvals
subscriptionId: azerty-a628-43e2-456f-1f9ea1b3ece3
tenantId: qwerty-5162-f14d-ab57-a0235a2385e0
clientId: benoit-820a-404b-efed-4cf7c0a99796
clientKey: p/v-Mmoussauda0yry3W7L3OB
````

```
$cp  ~/.aws/credentials ~/.xebialabs/aws.secrets.xlvals
$XL_VALUES_tfe_token="6SPlj2J5LMuw.atlasv1.Lm.........GWrnkSUZy1oCg"
$xl apply --xl-deploy-url http://localhost:4516 -f xebialabs.yaml 

[1/6] Applying infrastructure.yaml (imported by xebialabs.yaml)
    Updated CI Infrastructure/xebialabs-france/AWSProvider
    Updated CI Infrastructure/xebialabs-france

[2/6] Applying environment.yaml (imported by xebialabs.yaml)
    Updated CI Environments/dev
    Updated CI Environments/dev.conf
    Updated CI Environments/ec2-dictionary

[3/6] Applying applications.yaml (imported by xebialabs.yaml)
    Updated CI Applications/micro-vm/1.0.1/ec2
    Updated CI Applications/micro-vm/1.0.1
    Updated CI Applications/micro-vm/1.0.0/ec2
    Updated CI Applications/micro-vm/1.0.0
    Updated CI Applications/micro-vm

[4/6] Applying applications-bucket.yaml (imported by xebialabs.yaml)
    Updated CI Applications/s3-bucket/1.0.0/mybucket
    Updated CI Applications/s3-bucket/1.0.0
    Updated CI Applications/s3-bucket/1.0.1/mybucket
    Updated CI Applications/s3-bucket/1.0.1
    Updated CI Applications/s3-bucket

[5/6] Applying applications-content.yaml (imported by xebialabs.yaml)
    Updated CI Applications/s3-content/1.0.0/content
    Updated CI Applications/s3-content/1.0.0
    Updated CI Applications/s3-content/1.0.1/content
    Updated CI Applications/s3-content/1.0.1
    Updated CI Applications/s3-content

[6/6] Applying xebialabs.yaml
Done
```

if you look at a sample package that instantiates several Terraform modules, please look at 

```
xl apply -f xebialabs/aws_module.yaml
```
## Features


### Mappers

Once the cloud infrastructure generated & created, it is not over: the application needs to be deployed on top of. So the plugin offers to define customer mappers allowing creating new containers and added them to the environment.
A mapper is a python class extending ResourceMapper with 2 methods:
* the `accepted_types` method returns the list of the Terraform accepted_type.
* the `create_ci` method that build the list of the new CI that need to be created and added. The plugin managed to the updates and the deletions.

Then the mapper should be added to the `terraformEnterprise.Provider` using the `additionalMappers` map property. The key is a unique identifier, the value the path to the class. eg `xldtfe.mapper.aws_s3_mapper.AWSS3Mapper`

see sample code : https://github.com/xebialabs-community/xld-terraform-enterprise-plugin/blob/master/src/main/resources/xldtfe/mapper/aws_s3_mapper.py


### Structured Terraform Configured Items.

Even it's possible to package `terraform.InstantiatedModuleSpec` using a generic type, it's also possible to defined new CI based typed to help the user to fill the inputs & output properties.

Example. If you want to package the [jclopeza/java-bdd-project](https://registry.terraform.io/modules/jclopeza/java-bdd-project/module/4.0.0) module using a structured type, this is the definition you can add to the synthetic.xml file

```
<type type="jclopeza.JavaDBProject" extends="terraform.AbstractedInstantiatedModule"
      deployable-type="jclopeza.JavaDBProjectSpec" container-type="terraform.Configuration">
    <generate-deployable type="jclopeza.JavaDBProjectSpec" extends="terraform.AbstractedInstantiatedModuleSpec" copy-default-values="true"/>

    <property name="source" default="jclopeza/java-bdd-project/module" hidden="true"/>
    <property name="version" required="true" default="4.0.0"/>

    <!-- simple type -->
    <property name="aws_region" default="us-east-1" category="Input"/>
    <property name="environment" default="dev" category="Input"/>
    <property name="instance_type" default="t2.micro" category="Input"/>
    <property name="private_key_path" default="/dev/nul" category="Input" password="true"/>
    <property name="project_name" category="Input"/>
    <property name="public_key_path" category="Input"/>
    <property name="instance_type" label="InstanceType" default="t2.micro" category="Input"/>

    <!-- output-->
    <property name="public_ip_bdd" category="Output" required="false"/>
    <property name="public_ip_front" required="false" category="Output"/>

</type>
```

It's also possible to define structured types for `terraform.EmbeddedModule` helping to manage complex inputs & outputs.

```
  <type type="myaws.ec2.VirtualMachine" extends="terraform.AbstractedInstantiatedModule"
          deployable-type="myaws.ec2.VirtualMachineSpec" container-type="terraform.Configuration">
        <generate-deployable type="myaws.ec2.VirtualMachineSpec" extends="terraform.AbstractedInstantiatedModuleSpec" copy-default-values="true"/>

        <!-- simple type -->
        <property name="key_name" label="KeyName" category="Input"/>
        <property name="subnet_id" label="SubNet Id" category="Input"/>
        <property name="vpc_id" label="VPC Id" category="Input"/>
        <property name="secretPassword" category="Input" password="true"/>
        <property name="memory" category="Input" kind="integer"/>
        <property name="highLoad" category="Input" kind="boolean" default="true"/>
        <property name="instance_type" label="InstanceType" default="t2.micro" category="Input"/>

        <!-- complex type -->
        <property name="terraformTags" kind="map_string_string" category="Input" required="false"/>
        <property name="loadBalancerZone" kind="list_of_string" category="Input" required="false"/>

        <!-- output-->
        <property name="arn" label="ARN" category="Output" required="false"/>
        <property name="private_ip" label="Private IP" required="false" category="Output"/>
        <property name="security_group_id" label="Security Group Id" required="false" category="Output"/>
        <property name="secret_password" label="Sensitive Info" password="true" required="false" category="Output"/>
    </type>

    <type type="myaws.ec2.BlockDevice" extends="terraform.MapInputVariable"
          container-type="terraform.InstantiatedModule" deployable-type="myaws.ec2.BlockDeviceSpec">
        <generate-deployable type="myaws.ec2.BlockDeviceSpec" extends="terraform.MapInputVariableSpec"/>
        <property name="device_name" label="Device Name" category="Input"/>
        <property name="volume_size" label="Volume Size" category="Input"/>
    </type>

```

Full Sample is available [samples/synthetic.xml](samples/synthetic.xml).

### Annotation to link 2 modules

Typically, using input variables (module2) whose values is the output of the other one (module1).
```
 modules:
    - name: module2
      type: terraform.InstantiatedModuleSpec
      source: s3
      inputVariables:
        anothervar1: module.module1.anothervar1
      inputHCLVariables:        
        region: module.module1.region
```

the plugin offers an annotation if the 2 variables (input/output) have the same name: `<<module`
this annotation can be used with the `inputVariables` and `inputHCLVariables` properties.
this annotation is also manage to new types inheriting from `terraform.MapInputVariable` type. (cf [samples/synthetic.xm](samples/synthetic.xml))

```
 modules:
    - name: module2
      type: terraform.InstantiatedModuleSpec
      source: s3
      inputVariables:
        anothervar1: <<module1
      inputHCLVariables:        
        region: <<module1
```


### MapInputVariable

Often it's necessary to provide complex values as input variables. Either it's possible to use 
* `InstantiatedModule.inputHCLVariables` to provide the value as text.
* `terraform.MapInputVariableSpec` to provide values as ,easier to display and to manage values using dictionaries.
    * if an item has `name` that ends with '__' and a number, it will be merged the others to turn the value into a array of map "[{...},{....}]"
    * the number should start with 0 (zero) 

#### Example
if you package this
```
mapInputVariables:
  - name: ec2_block_device__2
    type: terraform.MapInputVariableSpec
    variables:
      size: 500Mo
      fs: FAT32
  - name: ec2_block_device__1
    type: terraform.MapInputVariableSpec
    variables:
      size: 2G
      fs: NTFS
  - name: tags
    type: terraform.MapInputVariableSpec
    variables:
      app: petportal
      version: 12.1.2
```
the plugin generates the following content:
```
module "s3-bucket" {
    source = "./s3"
    name="benoit.moussaud.bucket"
    region="eu-west-3"

    ec2_block_device=[{"fs": "NTFS", "size": "2G"}, {"fs": "FAT32", "size": "500Mo"}]
    tags={"app": "petportal", "version": "12.1.2"}
}
```
You may control the regexp by modifying the `mapArrayRegexp` defined in `terraform.InstantiatedModule` as an hidden property.

The default value is : `([a-zA-Z_1-9]*)__(\d+)`. Ex: outputVariablesmple: vol_1, vol_2, efs2_4,....

### Control task : Process Module
On the `terraform.Module` deployable CI, a `Process Module` control task allows to automatically fills the terraform modules with the variables defined in.
it fills only with the variables that has no default value or null value or empty value ({} or []).

### How to define a new provider

A provider gathers the properties used to configure and to authenticate the actions on a cloud provider as environment variables injected at deployment time.
Workflow:
1. create a new CI extending `terraformEnterprise.Provider`
2. add properties. Using the `password` attribut to control if it's a sensitive value or not.
3. fill the `credentialsPropertyMapping` default value that map each property name wth the environment variable name.

Sample: for AWS.
```
 <type type="terraformEnterprise.AwsProvider" extends="terraformEnterprise.Provider">
    <property name="accesskey" kind="string"  label="Access Key ID"  description="The access key to use when connecting to AWS(AWS_ACCESS_KEY_ID)."/>
    <property name="accessSecret" kind="string"   label="Secret Access Key" password="true"  description="The access secret key to use when connecting to AWS (AWS_SECRET_ACCESS_KEY)." />
    <property name="credentialsPropertyMapping" kind="map_string_string" hidden="false" default="accesskey:AWS_ACCESS_KEY_ID, accessSecret:AWS_SECRET_ACCESS_KEY" category="Parameters"/>
  </type>
```

## References

## How to release a new  candidate version

```
$./gradlew candidate
```

This command automaticaly tags the version, pushes it remotely and
trigger a release build. The script: `./buildViaTravis.sh` manages to
run the right command.

## How to release a new version

```
$./gradlew final
```

This command automaticaly tags the version, pushes it remotely and
trigger a release build. The script: `./buildViaTravis.sh` manages to
run the right command.

Icons made by <a href="https://www.flaticon.com/authors/dave-gandy" title="Dave Gandy">Dave Gandy</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>