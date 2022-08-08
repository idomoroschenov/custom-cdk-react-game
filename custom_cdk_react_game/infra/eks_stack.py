import yaml

from aws_cdk import (
    Stack,
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct


class EksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, network_props, eks_props, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        mainEKS = eks.Cluster(self, "MainEKS",
                              cluster_name="MainEKS",
                              version=eks.KubernetesVersion.V1_21,
                              default_capacity_instance=ec2.InstanceType.of(
                                    ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM),
                              default_capacity=3,
                              masters_role=iam.Role.from_role_name(
                                  self, "AdminRole", self.node.try_get_context("admin_role_name")),
                              alb_controller=eks.AlbControllerOptions(
                                  version=eks.AlbControllerVersion.V2_4_1
                              ),
                              vpc=network_props['vpc'],
                              vpc_subnets=[ec2.SubnetSelection(
                                  subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT)]
                              )

        self.output_props = eks_props.copy()
        self.output_props["eks_cluster"] = mainEKS

        CfnOutput(self, "Aws-auth", value=mainEKS.aws_auth.to_string())

    @property
    def outputs(self):
        return self.output_props
