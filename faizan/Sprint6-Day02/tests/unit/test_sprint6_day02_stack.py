import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint6_day02.sprint6_day02_stack import Sprint6Day02Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint6_day02/sprint6_day02_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Sprint6Day02Stack(app, "sprint6-day02")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
