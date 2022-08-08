import aws_cdk as cdk
from constructs import Construct
from ..infra.eks_stack import EksStack
from ..infra.network_stack import NetworkStack
from ..infra.ecr_stack import EcrStack
from ..application.app_stack import ApplicationStack 


class InfrastructureStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        network_props = {"namespace": "NetworkStack "}
        ecr_props = {"namespace": "EcrProps "}
        eks_props = {"namespace": "EksProps"}

        app = cdk.App()

        ecr = EcrStack(self, "EcrStack", ecr_props)
        ns = NetworkStack(self, "NetworkStack", network_props)
        eks = EksStack(self, "EksStack", ns.outputs, eks_props)

        app = ApplicationStack(self, "ApplicationStack", ecr.outputs, eks.outputs)
