> SkipQ Pegasus Python: Sprint 3 Project

# Creating a Multi-Stage CI/CD Pipeline having Beta/Gamma and Prod stages using CDK!

[![Linux](https://svgshare.com/i/Zhy.svg)](#) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](#) [![Generic badge](https://img.shields.io/badge/version-3.8.10-blue)](#)

### Objective

The objective of this Sprint3 is to build up on Sprint2 and create a multi-stage pipeline having Beta/Gamma and Prod stage using CDK and also deploy the project code in one or multiple regions. The core objectives are listed as follows:

* The Each stage must have bake Times, code-review, and test blockers.
* Write unit/integration tests for the web crawler.
* Emit CloudWatch metrics and alarms for the operational health of the web crawler, including memory and time-to-process each crawler run.
* Automate rollback to the last build if metrics are in alarm. Manage README files and run-books in markdown on GitHub.

### End Goal

The end goal of this sprint was to automate the build and deploy process of th Web Health Monitoring application using a multi-stage pipeline. For this purpose, I created a multi-stage pipeline architecture and added source and build artifact. I created alpha stage for unit testing and prod stage for manual approval and added them to the pipeline. The unit tests were created for alpha stage to check each unit of the application before deployment. At the end, I created metric and alarm at deployment satge and configured the Lambda deployment and rollback using deployment groups.

### TECHNOLOGIES USED

* AWS CI/CD Pipeline
* AWS CloudWatch
* AWS CodeBuild
* AWS CodePipeline
* AWS CloudWatch
* Github

## Documentation

The documentation is available on [GitHub](https://github.com/muhammadfaizan2022skipq/SkipQ-Documentation/blob/main/Faizan_Sprint3_Documentation.pdf).

> The full procedure to setup AWS and RUN the Sprint3 is given in next step.

## Environment Setup

* First install Windows Subsystem for Linux (WSL). For  this, download WSL.exe file from Google. I faced error in installtion using `wsl --install` command so I used `wsl.exe --install -d Ubuntu-20.04` commad to install it correctly.
* Dwnloaded VS Code and setup remote WSL from windows
* Download python3
* Donwload awscliv2.zip file from given path and install AWS. If you download it directly from google, there will be issue of path.
* Download and install NVM and NPM
* Check versions of all to be sure that softwares are installed corrrectly.

## How to Run

* Oopen the ubuntu terminal and clone the git repository using git clone 
* Confirm that your working directory is Sprint3
* Activate the virtual environment using command `source .venv/bin/activate`
* Now pip run requirements.txt file to install all required packages
* Configure the aws using `aws configure` and add your email and username to global configuration using command `git config --global user.email "your-email.gmail.com"` and `git config --global user.name "your-name"`.
* Synth and Deploy the project on Consile using `cdk synth` and `cdk deploy`.


## AWS Console

* Go to the AWS Console and monitore logs of WHLambda function for Availability and Latency.
* Go to the AWS Console and monitore logs of DBLambda function for records (if you print them).
* Go to the AWS DynamoDB database and check the item tables for records.
* Go to the AWS CodePipeline and check the deployment of all stages.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
 * `source .venv/bin/activate`        activate virtual environment
 * `pip install -r requirements.txt`  install requirements

> For a more in-depth getting started guide, visit the [Getting Started](https://docs.aws.amazon.com/codepipeline/latest/userguide/getting-started-codepipeline.html) page in the AWS docs.
