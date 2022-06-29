import aws_cdk as core
import aws_cdk.assertions as assertions
from aws_cdk.assertions import Match
import pytest

from sprint3.sprint3_stack import Sprint3Stack

# class Tests:
#     def __init__(self, app, stack, template):
#         self.app = app
#         self.stack = stack
#         self.app = app

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint3/sprint3_stack.py

def test_to_json():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    # Assert that the CloudFormation template deserialized into an object
    template.to_json()


def test_resources_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    # Assert that we have created 2 Lambda
    template.resource_count_is("AWS::Lambda::Function", 2)
    # Assert that we have created any S3 bucket
    template.resource_count_is("AWS::S3::Bucket", 0)
    # Assert that we have created 2 subscriptions
    template.resource_count_is("AWS::SNS::Subscription", 2)
    # Assert that we have created a table
    template.resource_count_is("AWS::DynamoDB::Table", 1)
    # Assert that we have created 8 alarms
    template.resource_count_is("AWS::CloudWatch::Alarm", 8)

def test_role_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.has_resource_properties(
        "AWS::IAM::Role",
        Match.object_equals(
            {
                "AssumeRolePolicyDocument": {
                    "Statement": [
                        {
                            "Action": "sts:AssumeRole",
                            "Effect": "Allow",
                            "Principal": {
                                "Service": "lambda.amazonaws.com"
                            }
                        }
                    ],
                "Version": "2012-10-17"
                },
                "ManagedPolicyArns": [
                    {
                        "Fn::Join": [
                            "",
                            [
                                "arn:",
                                {
                                "Ref": "AWS::Partition"
                                },
                                ":iam::aws:policy/CloudWatchFullAccess"
                                ]
                            ]
                        },
                {
                    "Fn::Join": [
                    "",
                    [
                        "arn:",
                        {
                        "Ref": "AWS::Partition"
                        },
                        ":iam::aws:policy/AmazonDynamoDBFullAccess"
                        ]
                    ]
                }
            ]
            }
        ),
    )


def test_alarm_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::CloudWatch::Alarm",
        {
            "Namespace": "FaizanAWS",
            "MetricName": Match.any_value(),
            "Dimensions": [
                {
                    "Name": "URL",
                    "Value": Match.any_value(),
                },
            ],
        },
    )


def test_table_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.has_resource_properties(
        "AWS::DynamoDB::Table",
        Match.object_equals(
            {
                "KeySchema": [
                {
                "AttributeName": "AlarmName",
                "KeyType": "HASH"
                },
                {
                "AttributeName": "AlarmTime",
                "KeyType": "RANGE"
                }
                ],
                "AttributeDefinitions": [
                {
                "AttributeName": "AlarmName",
                "AttributeType": "S"
                },
                {
                "AttributeName": "AlarmTime",
                "AttributeType": "S"
                }
                ],
                "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
                }
            }
        ),
    )


def test_subscription_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.has_resource_properties(
        "AWS::SNS::Subscription",
        Match.object_equals(
            {
                "Protocol": "lambda",
                "TopicArn": {
                    "Ref": "AlarmNotificationB0D2F5CA"
                    },
                "Endpoint": {
                    "Fn::GetAtt": [
                        "DBFunctions42E69620",
                        "Arn"
                    ]
                }
            }
        ),
    )


def test_rule_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.has_resource_properties(
        "AWS::Events::Rule",
        Match.object_equals(
            {
                "ScheduleExpression": "cron(60 0 * * ? *)",
                "State": "ENABLED",
                "Targets": [
                    {
                        "Arn": {
                            "Fn::GetAtt": [
                                "WHFunctions1AE513AC",
                                "Arn"
                            ]
                        },
                        "Id": "Target0"
                    }
                ]
            }
        ),
    )
