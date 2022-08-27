> SkipQ Pegasus Python: Sprint 1 Project

# Creating Hello World Lambda Function Application!

[![Linux](https://svgshare.com/i/Zhy.svg)](#) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](#) [![Generic badge](https://img.shields.io/badge/version-3.8.10-blue)](#)

## About Sprint

In this Sprint1, we attended the orientation session and met with our instructors and trainers. The session was very informative and useful in getting started and learning about the training program.

* In first day, we watched a video about the The Intutive Programmer: Learning How to Learn for Programmers. This helped and inspired me to follow best programming practices and learn by my own.
* In second day, we learned about the AWS Services, AWS regions and availability zones, SaaS vs PaaS vs IaS, What is the difference and how to choose the service.
* The third day was all about the AWS CDK setup on our local machine. We also learned about the EC2, Instances, AMIs and EC2 Regions & Zones, CloudFormation and basics of Linux.
* In 4th day of this sprint, we setup our CDK and created our First Lambda Function. This Lambda was deployed on AWS using CDK and CloudFormation template. We learned about the AWS CDK, Constructs, Apps, Stacks and Environment. We also learned about the AWS Lambda and its Concepts.

* On each day, we solved Leetcode problems as part of our interview preparation and also watched non-tech content.

* The full procedure to setup AWS and RUN the First Lambda function is given in next step.

## Environment Setup

* First install Windows Subsystem for Linux (WSL). For  this, download WSL.exe file from Google. I faced error in installtion using `wsl --install` command so I used `wsl.exe --install -d Ubuntu-20.04` commad to install it correctly.
* Dwnloaded VS Code and setup remote WSL from windows
* Download python3
* Donwload awscliv2.zip file from given path and install AWS. If you download it directly from google, there will be issue of path.
* Download and install NVM and NPM
* Check versions of all to be sure that softwares are installed corrrectly.

## How to Run

* After installing Linux Ubuntu, open the ubuntu terminal
* Clone your Forked repository from GitHub
* Go to your main cloned directory and create a new directory of your name
* Go to your name directory and create Sprint1 directory inside it.
* Open Visual Studio Code using `code .`
* Create a CDK Project inside your Sprint1
* At this stage, there will be issue of Virtual Environmet setup. To resolve this, install Virtual Environment from the commands provided in error message.
* Activate the virtual environment now using command `source .venv/bin/activate`
* Now pip run requirements.txt file to install all required packages
* From NPM, install aws-cdk
* Now add and commmit your files to GitHub repositiry
* To solve the issue of configuration, add your email and username to global configuration using command `git config --global user.email "your-email.gmail.com"` and `git config --global user.name "your-name"` and then commit changes again.

## Lambda Function

* Go to VS Code and Write your Lambda function in `sprint1_stack.py` file.
* Create a new folder and write code for `lambda_handler` in .py file
* Use `cdk synth` to synth your app on AWS
* Use `cdk deploy` to deploy your app on AWS
* Test your Lambda Function on Cloud

## AWS Console

* Go to the AWS Console and monitore logs of HelloWorld function.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
 * `source .venv/bin/activate`        activate virtual environment
 * `pip install -r requirements.txt`  install requirements

> For a more in-depth getting started guide, visit the [Getting Started](https://docs.aws.amazon.com/codepipeline/latest/userguide/getting-started-codepipeline.html) page in the AWS docs.
