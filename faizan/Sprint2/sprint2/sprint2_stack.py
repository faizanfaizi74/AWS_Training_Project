from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_, 
    RemovalPolicy, 
    aws_events as events_,
    aws_events_targets as targets_,
    aws_cloudwatch as cloudwatch_,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_cloudwatch_actions as cw_actions_,
    aws_sns_subscriptions as subscriptions_
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
        
        # Creating an SNS Topic
        # https://docs.aws.amazon.com/cdks/api/v1/python/aws_cdk.aws_sns/Topic.html
        topic = sns_.Topic(self, "AlarmNotification")
        #topic.apply_removal_policy(RemovalPolicy.DESTROY)

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
        email_address = "muhammadfaizan.ikram.skipq@gmail.com"
        topic.add_subscription(subscriptions_.EmailSubscription(email_address))
        
        for url in constants.URL_TO_MONITOR:
            # code for links here

            # creating Metric for Availability
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
            dimensions = {"URL" : url}

            availMetric = cloudwatch_.Metric(metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,
            namespace=constants.URL_MONITOR_NAMESPACE,
            dimensions_map=dimensions,
            period=Duration.minutes(1)
            )

            # define threshold and create Alarms for Availability metric
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
            availAlarm = cloudwatch_.Alarm(self, "AvailabilityAlarmfor_"+url,
                comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                threshold=1,
                evaluation_periods=1,
                metric=availMetric
            )
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            availAlarm.add_alarm_action(cw_actions_.SnsAction(topic))

            # creating Metric for Latency
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
            latenMetric = cloudwatch_.Metric(metric_name=constants.URL_MONITOR_NAME_LATENCY,
            namespace=constants.URL_MONITOR_NAMESPACE,
            dimensions_map=dimensions,
            period=Duration.minutes(1)
            )

            # define threshold and create Alarms for Latency metric
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
            latenAlarm = cloudwatch_.Alarm(self, "LatencyAlarmfor_"+url,
                comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                threshold=0.2,
                evaluation_periods=1,
                metric=latenMetric
            )
            latenAlarm.add_alarm_action(cw_actions_.SnsAction(topic))

    def create_lambda(self, id_, handler, path, myRole):
        return lambda_.Function(self, id_,
        runtime=lambda_.Runtime.PYTHON_3_8,
        handler=handler,
        code=lambda_.Code.from_asset(path),
        role=myRole,
        timeout=Duration.seconds(25),
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