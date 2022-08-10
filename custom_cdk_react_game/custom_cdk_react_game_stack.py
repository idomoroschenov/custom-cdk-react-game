import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep, CodeBuildOptions
from .stages.infra_stage import InfrastructureStage
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_codebuild as codebuild


class PipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        code_build_vpc = ec2.Vpc(self, "VPC",
                                 vpc_name="CodeBuildVpc",
                                 cidr="192.168.0.0/16",
                                 nat_gateways=1
                                 )

        pipeline = CodePipeline(self, "BuildPipeline",
                                pipeline_name="BuildPipeline",
                                synth=ShellStep("Synth",
                                                input=CodePipelineSource.git_hub(
                                                    f"{self.node.try_get_context('account_name')}/{self.node.try_get_context('repository_name')}", f"{self.node.try_get_context('branch_name')}"),
                                                commands=["npm install -g aws-cdk",
                                                          "python -m pip install -r requirements.txt",
                                                          "cdk synth"]),
                                code_build_defaults=CodeBuildOptions(vpc=code_build_vpc,
                                                                     subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT))

                                )

        deploy_infra = pipeline.add_stage(
            InfrastructureStage(self, "DeployInfrastructure"))
