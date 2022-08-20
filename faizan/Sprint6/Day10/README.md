
> SkipQ Pegasus Python: Sprint 6 Project Day 10

# Application Design!

[![Linux](https://svgshare.com/i/Zhy.svg)](#) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](#) [![Generic badge](https://img.shields.io/badge/version-3.8.10-blue)](#)

## Overview

### Design Problem:

![DesignProblem](https://github.com/muhammadfaizan2022skipq/Pegasus_Python/blob/main/faizan/Sprint6/Day10/image.png)

**Design & Develop** - A customer sends a request to an API Gateway endpoint. He wants a PDF report to be generated in return. The problem is the max response time of API Gateway is 30 seconds. The API Gateway is configured with a Lambda function that is responsible for performing the process of generating PDF reports. Imagine, the customer wants a report of a huge chunk of data and the processing time that the lambda will take can exceed 5 mins. The API Gateway can crash if its processing/response time exceeds 30 secs. How would you tackle such a problem? The API Gateway processing time is less than what the lambda function will take to perform the pdf generation process.
How we can manage to generate PDF report without making the API Gateway crash. How would you tackle such a problem?

> This project is the part of Sprint6 which has different design problems.

### Application Design

![ApplicationDesign](https://github.com/muhammadfaizan2022skipq/Pegasus_Python/blob/main/faizan/Sprint6/Day10/design-day10.png)

### Design Explanation - Demo
The design is explained in the following video. Feel free to share your thoughts!

* [Demo_Video](https://www.loom.com/share/7095dea133354d8694c3fd1aae54b44c)

### TECHNOLOGIES USED

* [AWS S3](https://aws.amazon.com/s3/)
* [AWS Lambda](https://aws.amazon.com/lambda/)
* [AWS API Gateway](https://aws.amazon.com/api-gateway/)
* [AWS DynamoDB](https://aws.amazon.com/dynamodb/)
* [AWS SES](https://aws.amazon.com/ses/)
* [AWS IAM](https://aws.amazon.com/iam/)
* [AWS GitHub](https://github.com/aws-samples)


> For a more in-depth guide, visit the [Getting Started](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html) page in the AWS docs.
