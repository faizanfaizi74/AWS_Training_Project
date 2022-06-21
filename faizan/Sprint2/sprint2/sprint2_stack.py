from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_, 
    RemovalPolicy, 
    aws_events as events_,
    aws_events_targets as targets_,
    aws_cloudwatch as cloudwatch_,
    aws_iam as iam_
)
from constructs import Construct
from resources import constants as constants

class Sprint2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # creating ,y lambda function for deploying WHLambda.py
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html
        lambda_role = self.create_role()
        WHLambda = self.create_lambda("WH_Functions", "WHLambda.lambda_handler", "./resources", lambda_role)

        # policy for destroying resources
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/RemovalPolicy.html#aws_cdk.core.RemovalPolicy
        WHLambda.apply_removal_policy(RemovalPolicy.DESTROY)

        # scheduling the lambda function
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Schedule.html
        schedule = events_.Schedule.cron(minute="0/1")
        target = targets_.LambdaFunction(handler=WHLambda)
        
        rule = events_.Rule(self, "LambdaEventRule",
            schedule=schedule,
            targets=[target]
        )
        
        # creating Metric for Availability
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
        dimensions = {"URL": constants.URL_TO_MONITOR}

        availMetric = cloudwatch_.Metric(metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,
        namespace=constants.URL_MONITOR_NAMESPACE,
        dimensions_map=dimensions,
        label="Availability",
        period=Duration.minutes(1),)

        # define threshold and create Alarms for Availability metric
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        availAlarm = cloudwatch_.Alarm(self, "AvailabilityAlarm",
            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            threshold=1,
            evaluation_periods=1,
            metric=availMetric
        )

        # creating Metric for Latency
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
        latenMetric = cloudwatch_.Metric(metric_name=constants.URL_MONITOR_NAME_LATENCY,
        namespace=constants.URL_MONITOR_NAMESPACE,
        dimensions_map=dimensions,
        label="Latency",
        period=Duration.minutes(1),)

        # define threshold and create Alarms for Latency metric
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        latenAlarm = cloudwatch_.Alarm(self, "LatencyAlarm",
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=0.2,
            evaluation_periods=1,
            metric=latenMetric
        )

    def create_lambda(self, id_, handler, path, myRole):
        return lambda_.Function(self, id_,
        runtime=lambda_.Runtime.PYTHON_3_8,
        handler=handler,
        code=lambda_.Code.from_asset(path),
        role=myRole,
        )

    # creating role for policies
    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/ManagedPolicy.html
    # input parameters: None
    # return values: lambda_role
    def create_role(self):
        lambda_role = iam_.Role(self, "Role",
        assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
        managed_policies=[
            iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess")
            ]
        )
        return lambda_role


