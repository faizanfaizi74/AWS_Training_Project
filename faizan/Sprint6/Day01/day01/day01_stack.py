from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_, 
    RemovalPolicy, 
    aws_cloudwatch as cloudwatch_,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_cloudwatch_actions as cw_actions_,
    aws_sns_subscriptions as subscriptions_,
    aws_dynamodb as dynamodb_,
    aws_apigateway as apigateway_,
)
from constructs import Construct
from resources import constants as constants

class Day01Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create lambda functions
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html
        lambda_role = self.create_role()
        APILambda = self.create_lambda("API_Functions", "APILambda.lambda_handler", "./resources", lambda_role)
        
        # create an SNS Topic to send email notification
        # https://docs.aws.amazon.com/cdks/api/v1/python/aws_cdk.aws_sns/Topic.html
        topic = sns_.Topic(self, "AlarmNotification")

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
        topic.add_subscription(subscriptions_.EmailSubscription(constants.SNS_EMAIL_ADDRESS))

        ############################################    API Gateway Integration     ############################################ 
    
        # create REST API Gateway integrated with `APILambda backend`
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/LambdaRestApi.html
        api = apigateway_.LambdaRestApi(self, id = "FaizanAPI",
                handler= APILambda,
                proxy=False,
                endpoint_configuration= apigateway_.EndpointConfiguration(
                types= [apigateway_.EndpointType.REGIONAL]
            )
        )

        # define API Gateway permissions to invoke  APIlambda
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html?highlight=grant%20invoke#aws_cdk.aws_lambda.Function.grant_invoke
        APILambda.grant_invoke(iam_.ServicePrincipal("apigateway.amazonaws.com"))

        # add resource and methods
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/Resource.html
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/IResource.html#aws_cdk.aws_apigateway.IResource.add_method
        root = api.root.add_resource("root")       # path to resource
        root.add_method("POST")                    # POST: (Create) /root 

        ##################################################################################################################

        # creating Metric for value
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Metric.html
        valueMetric = cloudwatch_.Metric(metric_name=constants.VALUE_MONITOR_NAME_RESPONSE,
            namespace=constants.VALUE_MONITOR_NAMESPACE,
            dimensions_map={"ARG1" : "arg1"},
            period=Duration.minutes(1)
        )

        # define threshold and create Alarms for Value
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch/Alarm.html
        valueAlarm = cloudwatch_.Alarm(self, "ValueAlarm",
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=10,
            evaluation_periods=1,
            metric=valueMetric,
            datapoints_to_alarm=1,
        )

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
        valueAlarm.add_alarm_action(cw_actions_.SnsAction(topic))

        # Removal policy to destroy services
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/RemovalPolicy.html#aws_cdk.core.RemovalPolicy
        APILambda.apply_removal_policy(RemovalPolicy.DESTROY)
        topic.apply_removal_policy(RemovalPolicy.DESTROY)
        api.apply_removal_policy(RemovalPolicy.DESTROY)

    # input parameters: id, handler, path and role
    # return values: Lambda function
    def create_lambda(self, id_, handler, path, myRole):
        return lambda_.Function(self, id_,
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler=handler,
            code=lambda_.Code.from_asset(path),
            role=myRole,
            timeout=Duration.seconds(100),
        )
        
    # creating role for policies
    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/ManagedPolicy.html
    # input parameters: None
    # return values: lambda_role
    def create_role(self):
        return iam_.Role(self, "Role",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess")
                ]
            )
            