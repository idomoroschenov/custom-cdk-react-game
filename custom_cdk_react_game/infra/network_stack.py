from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct


class NetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, network_props, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "VPC",
                      vpc_name="Main",
                      cidr="192.168.0.0/16"
                      )
        self.output_props = network_props.copy()
        self.output_props['vpc'] = vpc

    @property
    def outputs(self):
        return self.output_props
