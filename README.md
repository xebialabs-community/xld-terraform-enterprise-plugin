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
$cp cp  ~/.aws/credentials ~/.xebialabs/aws.secrets.xlvals
$xl apply --xl-deploy-url http://localhost:4556 -f xebialabs.yaml --values tfe_token=XXXXXXXX


```
## Features

## References

