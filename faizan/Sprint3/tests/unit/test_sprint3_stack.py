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

# Tests for Cloudformation Template

def test_to_json():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    # Assert that the CloudFormation template deserialized into an object
    template.to_json()


def test_lambda_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    # Assert that we have created 2 Lambda
    template.resource_count_is("AWS::Lambda::Function", 2)

def test_subscription_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    # Assert that we have created 2 subscriptions
    template.resource_count_is("AWS::SNS::Subscription", 2)

def test_table_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    # Assert that we have created a table
    template.resource_count_is("AWS::DynamoDB::Table", 1)

def test_role_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.has_resource_properties(
        "AWS::IAM::Role",
            {
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
    )

def test_composite_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.has_resource_properties(
        "AWS::DynamoDB::Table",
            {
                "KeySchema": [
                   {
                     "AttributeName": "MetricName",
                     "KeyType": "HASH"
                   },
                   {
                     "AttributeName": "Timestamp",
                     "KeyType": "RANGE"
                   }
                ],
            }
    )


def test_lambda_subscription_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.has_resource_properties("AWS::SNS::Subscription", {"Protocol": "lambda"})


def test_email_subscription_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.has_resource_properties("AWS::SNS::Subscription", {"Protocol": "email"})
    

def test_rule_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.has_resource_properties(
        "AWS::Events::Rule",
            {
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
        )
