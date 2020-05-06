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
## Features

### MapInputVariable

Often it's necessary to provide complex values as input variables. Either it's possible to use 
* `InstantiatedModule.inputHCLVariables` to provide the value as text.
* `terraform.MapInputVariableSpec` to provide values as ,easier to display and to manage values using dictionaries.
    * if an item has `name` that ends with '__' and a number, it will be merged the others to turn the value into a array of map "[{...},{....}]"
    * the number should start with 0 (zero) 

__TODO: PASTE SAMPLE__
__TODO: PASTE SAMPLE__
__TODO: PASTE SAMPLE__

### Control task : Process Module
On the `terraform.Module` deployable, a `Process Module` control task allows to automatically fills the terraform modules with the variables defined in.
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

## How to release a new version

```
$./gradlew final
```

This command automaticaly tags the version, pushes it remotely and
trigger a release build. The script: `./buildViaTravis.sh` manages to
run the right command.

