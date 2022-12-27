from aws_cdk import (
    Stack,
)
import aws_cdk as cdk
from constructs import Construct

class WithDependenciesStack(Stack):
    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        resource_provider_service_token: str,
        number_of_resources: int,
        version: str,
        **kwargs) -> None:
        
        super().__init__(scope, construct_id, **kwargs)

        previous_resource = None

        for i in range(1, number_of_resources+1):
          resource = cdk.CustomResource(
            self,
            f"custom-resource-{i}",
            service_token=resource_provider_service_token,
            properties={
              'ResourceName': f"resource-{i}",
              'ResourceVersion': version,
              'Approach': 'with_dependencies',
            }
          )
          
          if previous_resource:
            resource.node.add_dependency(previous_resource)

          previous_resource = resource

