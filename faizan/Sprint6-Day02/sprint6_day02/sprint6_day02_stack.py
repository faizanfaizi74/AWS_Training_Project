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

class Sprint6Day02Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create lambda functions
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html
        lambda_role = self.create_role()
        APILambda = self.create_lambda("API_Functions", "APILambda.lambda_handler", "./resources", lambda_role)
        
        # create table
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html 
        ResponseTable = self.create_API_table(constants.API_TABLE_NAME)

        # set environment variable
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html#aws_cdk.aws_lambda.Function.add_environment
        tName = ResponseTable.table_name
        APILambda.add_environment(key="RESPONSE_TABLE", value=tName)

        ############################################    Multiple API Gateway Integration     ############################################ 
    
        # create REST API Gateway integrated with `APILambda backend`
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/LambdaRestApi.html
        api_1 = apigateway_.LambdaRestApi(self, id = "FaizanAPI-1",
                handler= APILambda,
                proxy=False,
                endpoint_configuration= apigateway_.EndpointConfiguration(
                types= [apigateway_.EndpointType.REGIONAL]
            )
        )

        api_2 = apigateway_.LambdaRestApi(self, id = "FaizanAPI-2",
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
        root1 = api_1.root.add_resource("root")     # path to resource
        root1.add_method("POST")                    # POST: (CREATE) /root
        root1.add_method("GET")                     # GET: (READ) /root

        root2 = api_2.root.add_resource("root")     # path to resource
        root2.add_method("POST")                    # POST: (CREATE) /root
        root2.add_method("GET")                     # GET: (READ) /root  

        ##################################################################################################################

        # Removal policy to destroy services
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/RemovalPolicy.html#aws_cdk.core.RemovalPolicy
        APILambda.apply_removal_policy(RemovalPolicy.DESTROY)
        api_1.apply_removal_policy(RemovalPolicy.DESTROY)
        api_2.apply_removal_policy(RemovalPolicy.DESTROY)

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
    
    def create_API_table(self, id_):
        return dynamodb_.Table(self, id_,
            removal_policy=RemovalPolicy.DESTROY,
            partition_key= dynamodb_.Attribute(name= "attr1", type= dynamodb_.AttributeType.STRING),
            sort_key= dynamodb_.Attribute(name= "requestTime", type= dynamodb_.AttributeType.STRING),
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
            