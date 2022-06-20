from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_, 
    RemovalPolicy, 
    aws_events as events_,
    aws_events_targets as targets_
)
from constructs import Construct

class Sprint2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # creating ,y lambda function for deploying WHLambda.py
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html
        WHLambda = self.create_lambda("WH_Functions", "WHLambda.lambda_handler", "./resources")
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

    def create_lambda(self, id_, handler, path):
        return lambda_.Function(self, id_,
        runtime=lambda_.Runtime.PYTHON_3_8,
        handler=handler,
        code=lambda_.Code.from_asset(path)
        )

