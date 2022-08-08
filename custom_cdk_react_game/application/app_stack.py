import yaml

from aws_cdk import (
    Stack,
    aws_eks as eks,
)
from constructs import Construct


def read_yaml(yaml_path: str) -> dict:
    with open(yaml_path, 'r') as yaml_raw:
        return yaml.load(yaml_raw, yaml.Loader)


class ApplicationStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, ecr_props, eks_props, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        react_ns_config = read_yaml(
            "custom_cdk_react_game/application/react_resources/react_namespace.yaml")
        react_deploy_config = read_yaml(
            "custom_cdk_react_game/application/react_resources/react_deploy.yaml")
        react_deploy_config["spec"]["template"]["spec"]["containers"][0]["image"] = ecr_props["react_app_image_uri"]
        react_service_config = read_yaml(
            "custom_cdk_react_game/application/react_resources/react_service.yaml")
        react_ingress_config = read_yaml(
            "custom_cdk_react_game/application/react_resources/react_ingress.yaml")

        react_ns = eks.KubernetesManifest(
            self, "ReactNamespace", cluster=eks_props["eks_cluster"], manifest=[react_ns_config], overwrite=True)

        react_deploy = eks.KubernetesManifest(self, "ReactDeployment", cluster=eks_props["eks_cluster"], manifest=[
            react_deploy_config, react_service_config, react_ingress_config], overwrite=True)
        react_deploy.node.add_dependency(react_ns)
