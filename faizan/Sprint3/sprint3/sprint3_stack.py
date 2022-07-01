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
    aws_sns_subscriptions as subscriptions_,
    aws_dynamodb as dynamodb_,
    aws_codedeploy as codedeploy_,
)
from constructs import Construct
from resources import constants as constants

class Sprint3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # creating lambda function for deploying WHLambda.py and DBLambda.py
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html
        lambda_role = self.create_role()
        WHLambda = self.create_lambda("WH_Functions", "WHLambda.lambda_handler", "./resources", lambda_role)
        DBLambda = self.create_lambda("DB_Functions", "DBLambda.lambda_handler", "./resources", lambda_role)
  
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html

        DBTable = self.create_table()

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html#aws_cdk.aws_lambda.Function.add_environment
        tname = DBTable.table_name
        DBLambda.add_environment(key="Alarm_key", value=tname)  # Adding env variable

        # policy for destroying resources
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/RemovalPolicy.html#aws_cdk.core.RemovalPolicy
        WHLambda.apply_removal_policy(RemovalPolicy.DESTROY)
        DBLambda.apply_removal_policy(RemovalPolicy.DESTROY)

        # scheduling the lambda function
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Schedule.html
        schedule = events_.Schedule.rate(Duration.minutes(60)) # for every minute
        target = targets_.LambdaFunction(handler=WHLambda)
        
        rule = events_.Rule(self, "LambdaEventRule",
            schedule=schedule,
            targets=[target]
        )
        
        # Creating an SNS Topic
        # https://docs.aws.amazon.com/cdks/api/v1/python/aws_cdk.aws_sns/Topic.html
        topic = sns_.Topic(self, "AlarmNotification")

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
        email_address = "muhammadfaizan.ikram.skipq@gmail.com"
        topic.add_subscription(subscriptions_.EmailSubscription(email_address))
        # Lambda Subscription
        topic.add_subscription(subscriptions_.LambdaSubscription(DBLambda))

        #-------------------------------------------------------------Sprint #03 Stack Start---------------------------------------------------#

        #Step:01 Get the metric
        WHLambdaDurationMetric = WHLambda.metric("Duration", period=Duration.minutes(60))
        WHLambdaInvocationMetric = WHLambda.metric("Invocations", period=Duration.minutes(60))

        #Step:02 Create Alarms for metric
        durationAlarm = cloudwatch_.Alarm(self, "WHLambdaAlarmfor_Duration",
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=1,
            evaluation_periods=1,
            metric=WHLambdaDurationMetric,
            )

        invocationAlarm = cloudwatch_.Alarm(self, "WHLambdaAlarmfor_Invocation",
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=1,
            evaluation_periods=1,
            metric=WHLambdaInvocationMetric,
            )

        durationAlarm.add_alarm_action(cw_actions_.SnsAction(topic))
        invocationAlarm.add_alarm_action(cw_actions_.SnsAction(topic))

        # Lambda deployment configuration and rollback
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Alias.html#aws_cdk.aws_lambda.Alias
        version = WHLambda.current_version
        alias = lambda_.Alias(self, "Lambda_Faizan_Alias",
            alias_name="Prod_Faizan_Alias",
            version=version
        )

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html
        deployment_group = codedeploy_.LambdaDeploymentGroup(self, "FaizanLambdaDeployment",
            alias = alias,
            alarms = [durationAlarm, invocationAlarm],   
            deployment_config = codedeploy_.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE
        )

        #-------------------------------------------------------------Sprint #03 Stack End---------------------------------------------------#
                
        for url in constants.URL_TO_MONITOR:
            # creating Metric for Availability and Latency
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html

            availMetric = cloudwatch_.Metric(metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,
            namespace=constants.URL_MONITOR_NAMESPACE,
            dimensions_map={"URL" : url},
            period=Duration.minutes(constants.URL_TIME_CONSTANT)
            )

            latenMetric = cloudwatch_.Metric(metric_name=constants.URL_MONITOR_NAME_LATENCY,
            namespace=constants.URL_MONITOR_NAMESPACE,
            dimensions_map={"URL" : url},
            period=Duration.minutes(constants.URL_TIME_CONSTANT)
            )

            # define threshold and create Alarms for Availability and Latency metric
            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
            availAlarm = cloudwatch_.Alarm(self, "AvailabilityAlarmfor_"+url,
            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            threshold=1,
            evaluation_periods=1,
            metric=availMetric
            )

            latenAlarm = cloudwatch_.Alarm(self, "LatencyAlarmfor_"+url,
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=0.1,
            evaluation_periods=1,
            metric=latenMetric
            )

            # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            availAlarm.add_alarm_action(cw_actions_.SnsAction(topic))
            latenAlarm.add_alarm_action(cw_actions_.SnsAction(topic))


    # input parameters: id, handler, path and role
    # return values: Lambda function
    def create_lambda(self, id_, handler, path, myRole):
        return lambda_.Function(self, id_,
        runtime=lambda_.Runtime.PYTHON_3_8,
        handler=handler,
        code=lambda_.Code.from_asset(path),
        role=myRole,
        timeout=Duration.seconds(300),
        )

    # input parameters: None
    # return values: dynamo_db table
    def create_table(self):
        return dynamodb_.Table(self, "AlarmInfoTable",
            partition_key=dynamodb_.Attribute(name="AlarmID", type=dynamodb_.AttributeType.STRING),
            sort_key=dynamodb_.Attribute(name="AlarmTime", type=dynamodb_.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY
        )

    # creating role for policies
    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/ManagedPolicy.html
    # input parameters: None
    # return values: lambda_role
    def create_role(self):
        return iam_.Role(self, "Role",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")
                ]
            )
            