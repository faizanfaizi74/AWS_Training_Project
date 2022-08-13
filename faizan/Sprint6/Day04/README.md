
> SkipQ Pegasus Python: Sprint 6 Project Day 03

# Application Design!

[![Linux](https://svgshare.com/i/Zhy.svg)](#) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](#) [![Generic badge](https://img.shields.io/badge/version-3.8.10-blue)](#)

## Overview

### Design Problem:
Design and Develop: Deploy, maintain and rollback pipeline for an artifact deployment e-g lambda package, docker image etc.

> This project is the part of Sprint6 which has different design problems. The fourth day is about designing and developing a Codepipeline to automate test, build and deploy processes.

**A) What do you think if the latest deployment is failing?**

> The latest deployment can be failed due to multiple factors. Some of them are mentioned below:
> 1. A change in Policies: If the policies in AWS account are changed and there are provided role that does not have sufficient permissions, then the deployment of > latest version can be failed.
> 2. The source repo permissions are changed and not authorized to the repository.
> 3. The corrupt Cloudformation template can also casues the deploment to be failed

**B) How will you rollback?**

>CodeDeploy is used to roll back deployments by redeploying a previously deployed revision of an application as a new deployment. These rolled-back deployments are technically new deployments, with new deployment IDs, rather than restored versions of a previous deployment.
>
>Deployments can be rolled back automatically or manually. To auto rollback on previous version, we can define an "Alias" that points to the current version of the application and a "Deployment Group" that uses Blue-Green Deployment configuration. Whenever we face any problem in deployment or when a monitoring threshold we specify is met, the application will rollback to its previous version using the Alias and Deployment Group.

**C) How do you reduce such failures so there is less need to rollback?**

>Rollback triggers/alarms enable us to monitor the state of the application during stack creation and updating, and to rollback that operation if the application breaches the threshold of any of the alarms we've specified and goes into IN ALARM state.
>To redice the need of rollback, we should completely understand the design problem and requirements of an application. The the current requirements and future modifications such as traffic, regions etc should be clearly specified in the stack resources and service architecture, so the application can perform well in unexpected situations and does not go to IN ALARM state frequenctly due to poor architecture.


### Application Design

![ApplicationDesign](https://github.com/muhammadfaizan2022skipq/Pegasus_Python/blob/main/faizan/Sprint6/Day04/design-day04.png)

### TECHNOLOGIES USED

* [AWS Lambda](https://aws.amazon.com/lambda/)
* [AWS CodePipeline](https://aws.amazon.com/codepipeline/)
* [AWS Github](https://github.com/aws-samples)


> For a more in-depth guide, visit the [Getting Started](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html) page in the AWS docs.
