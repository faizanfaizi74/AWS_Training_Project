
> SkipQ Pegasus Python: Sprint 2 Project

# Web Health Monitoring and DynamoDB Management with Alarm Notifications!

[![Linux](https://svgshare.com/i/Zhy.svg)](#) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](#) [![Generic badge](https://img.shields.io/badge/version-3.8.10-blue)](#)

## About Sprint2

In this Sprint2, We created Lambda functions for Web Health Monitoring and Database Management

* We have created Lambda function to check the availability and latency of the website.
* We scheduled the lambda function for every minute to automate the process.
* The alarm notification for availability and latency was enabled by giving certain threshold and added subscription on email for each alarm.
* The record was stored in DynamoDB database table for the alarm notification for future reference and record.

* The full procedure to setup AWS and RUN the Sprint2 is given in next step.

## Environment Setup

* First install Windows Subsystem for Linux (WSL). For  this, download WSL.exe file from Google. I faced error in installtion using `wsl --install` command so I used `wsl.exe --install -d Ubuntu-20.04` commad to install it correctly.
* Dwnloaded VS Code and setup remote WSL from windows
* Download python3
* Donwload awscliv2.zip file from given path and install AWS. If you download it directly from google, there will be issue of path.
* Download and install NVM and NPM
* Check versions of all to be sure that softwares are installed corrrectly.

## How to Run

* Oopen the ubuntu terminal and clone the git repository using git clone 
* Confirm that your working directory is Sprint2
* Activate the virtual environment using command `source .venv/bin/activate`
* Now pip run requirements.txt file to install all required packages
* Configure the aws using `aws configure` and add your email and username to global configuration using command `git config --global user.email "your-email.gmail.com"` and `git config --global user.name "your-name"`.
* Synth and Deploy the project on Consile using `cdk synth` and `cdk deploy`.


## AWS Console

* Go to AWS Console and monitore logs of WHLambda function for Availability and Latency.
* Go to AWS Console and monitore logs of DBLambda function for records (if you print them).
* Go to DynamoDB database and check the item tables for records.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
 * `source .venv/bin/activate`        activate virtual environment
 * `pip install -r requirements.txt`  install requirements

Enjoy!
