from aws_cdk import (
    Stack,
    CfnOutput,
)
from constructs import Construct
from aws_cdk.aws_ecr_assets import DockerImageAsset
from os import path


class EcrStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, ecr_props, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        react_app = DockerImageAsset(self, "React",
                                      directory="custom_cdk_react_game/application/react-wordle",
                                      file="docker/Dockerfile"
                                      )
        
        self.output_props = ecr_props.copy()
        self.output_props["react_app_image_uri"] = react_app.image_uri

    @property
    def outputs(self):
        return self.output_props
