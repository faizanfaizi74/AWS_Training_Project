
import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint3.sprint3_stack import Sprint3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint3/sprint3_stack.py
def test_lambda_created():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)

    # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
    template.resource_count_is("AWS::Lambda::Function", 2)
    template.resource_count_is("AWS::S3::Bucket", 0)
