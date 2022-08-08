import aws_cdk as core
import aws_cdk.assertions as assertions

from custom_cdk_react_game.custom_cdk_react_game_stack import CustomCdkReactGameStack

# example tests. To run these tests, uncomment this file along with the example
# resource in custom_cdk_react_game/custom_cdk_react_game_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CustomCdkReactGameStack(app, "custom-cdk-react-game")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
