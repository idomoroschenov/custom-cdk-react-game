import aws_cdk as cdk
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from .stages.infra_stage import InfrastructureStage


class PipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline = CodePipeline(self, "BuildPipeline",
                                pipeline_name="BuildPipeline",
                                synth=ShellStep("Synth",
                                                input=CodePipelineSource.git_hub(
                                                    "idomoroschenov/custom-cdk-react-game", "main"),
                                                commands=["npm install -g aws-cdk",
                                                          "python -m pip install -r requirements.txt",
                                                          "cdk synth"]))

        deploy_infra = pipeline.add_stage(
            InfrastructureStage(self, "DeployInfrastructure"))
