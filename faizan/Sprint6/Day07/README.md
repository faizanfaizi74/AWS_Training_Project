
> SkipQ Pegasus Python: Sprint 6 Project Day 07

# Application Design!

[![Linux](https://svgshare.com/i/Zhy.svg)](#) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](#) [![Generic badge](https://img.shields.io/badge/version-3.8.10-blue)](#)

## Overview

### Design Problem:

![DesignProblem](https://github.com/muhammadfaizan2022skipq/Pegasus_Python/blob/main/faizan/Sprint6/Day07/image.png)

**Design & Develop** - Suppose there are 10 files uploading to S3 bucket each day. For each file received on cloud storage, you have a mechanism to process the file. During the processing, your code parses the text and counts the number of times each word is repeated in the file. For example, in the following text: “Hello World and Hello There”, your code should be able to say that "hello" has been used twice, "world" has occured once and so on. Then it will store the results in some storage and email to some email address after successful processing.

> This project is the part of Sprint6 which has different design problems.

### Application Design

![ApplicationDesign](https://github.com/muhammadfaizan2022skipq/Pegasus_Python/blob/main/faizan/Sprint6/Day07/design-day07.png)

### TECHNOLOGIES USED

* [AWS S3](https://aws.amazon.com/s3/)
* [AWS Lambda](https://aws.amazon.com/lambda/)
* [AWS DynamoDB](https://aws.amazon.com/dynamodb/)
* [AWS SNS](https://aws.amazon.com/sns/)
* [AWS IAM](https://aws.amazon.com/iam/)
* [AWS GitHub](https://github.com/aws-samples)


> For a more in-depth guide, visit the [Getting Started](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html) page in the AWS docs.
