
> SkipQ Pegasus Python: Sprint 6 Project Day 02

# Multiple API Gateway with DynamoDB Service!

[![Linux](https://svgshare.com/i/Zhy.svg)](#) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](#) [![Generic badge](https://img.shields.io/badge/version-3.8.10-blue)](#)

## Overview

This project is the part of Sprint5 which has different design problems. The second day is about building multiple public server-less API Gateway endpoint for the client to pass the event in a specific format and we have to parse the event in lambda fucntion to get the value and add it to DynamoDB database.

### End Goal

The end goal of this sprint is to build multiple public serverless API Gateway endpoint for the client to pass the event, extract value from it and also get the first 10 latest events from DynamoDB database table.

### Application Design


![Application Design](https://github.com/muhammadfaizan2022skipq/Pegasus_Python/blob/main/faizan/Sprint6-Day02/Sprint6-Day02.drawio.png)

### TECHNOLOGIES USED

* [AWS Lambda](https://aws.amazon.com/lambda/)
* [AWS API Gateway](https://aws.amazon.com/api-gateway/)
* [AWS Github](https://github.com/aws)


> The full procedure to setup AWS and RUN the Sprint6-Day02 is given in next step.

## Gettin Started - Environment Setup

1. First install Windows Subsystem for Linux (WSL). For  this, download WSL.exe file from Google. I faced error in installtion using `wsl --install` command so I used `wsl.exe --install -d Ubuntu-20.04` commad to install it correctly.
2. Dwnloaded VS Code and setup remote WSL from windows
3. Download python3
4. Donwload awscliv2.zip file from given path and install AWS. If you download it directly from google, there will be issue of path.
6. Download and install NVM and NPM
7. Check versions of all to be sure that softwares are installed corrrectly.

## Project Deployment - How to Run

1. Oopen the ubuntu terminal and clone the git repository using `git clone "forked-repo-github-url"`
2. Confirm that your working directory is `Sprint6-Day02`
3. Activate the virtual environment using command `source .venv/bin/activate`
4. Configure the aws using `aws configure` and add your email and username to global configuration using command

    ```sh
    git config --global user.email "your-email.gmail.com"
    ```
    and
    ```sh
    git config --global user.name "your-name"
    ```
5. Run `pip install -r requirements.txt` to install all required packages
6. Synth and Deploy the project on Consile using `cdk synth` and `cdk deploy`.

## How to contribute

If you'd like to contribute, start by searching through the [pull requests](https://github.com/muhammadfaizan2022skipq/Pegasus_Python/pulls) to see whether someone else has raised a similar idea or question.

If you don't see your idea listed, and you think it fits into the goals of this guide, open a pull request.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
 * `source .venv/bin/activate`        activate virtual environment
 * `pip install -r requirements.txt`  install requirements


> For a more in-depth guide, visit the [Getting Started](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html) page in the AWS docs.