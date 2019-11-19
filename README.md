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

## References

