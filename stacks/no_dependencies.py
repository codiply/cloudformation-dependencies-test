from aws_cdk import (
    Stack,
)
import aws_cdk as cdk
from constructs import Construct

class NoDependenciesStack(Stack):
    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        resource_provider_service_token: str,
        number_of_resources: int,
        version: str,
        **kwargs) -> None:
        
        super().__init__(scope, construct_id, **kwargs)

        for i in range(1, number_of_resources+1):
          cdk.CustomResource(
            self,
            f"custom-resource-{i}",
            service_token=resource_provider_service_token,
            properties={
              'ResourceName': f"resource-{i}",
              'ResourceVersion': version,
              'Approach': 'no_dependencies',
            }
          )

