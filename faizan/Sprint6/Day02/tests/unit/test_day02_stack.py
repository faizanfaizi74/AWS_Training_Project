import aws_cdk as core
import aws_cdk.assertions as assertions

from day02.day02_stack import Day02Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in day02/day02_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Day02Stack(app, "day02")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
