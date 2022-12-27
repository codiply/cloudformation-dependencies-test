from aws_cdk import (
    Stack,
    NestedStack
)
import aws_cdk as cdk
from constructs import Construct

class ResourceInNestedStack(NestedStack):
    def __init__(
      self, 
      scope: Construct, 
      construct_id: str, 
      resource_provider_service_token: str,
      resource_name: str,
      version: str,
      **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        cdk.CustomResource(
            self,
            f"custom-resource-{resource_name}",
            service_token=resource_provider_service_token,
            properties={
              'ResourceName': resource_name,
              'ResourceVersion': version,
              'Approach': 'nested_stack_with_dependencies',
            }
          )

class NestedStacksWithDependenciesStack(Stack):
    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        resource_provider_service_token: str,
        number_of_resources: int,
        version: str,
        **kwargs) -> None:
        
        super().__init__(scope, construct_id, **kwargs)

        previous_nested_stack = None

        for i in range(1, number_of_resources+1):
          nested_stack = ResourceInNestedStack(
            self,
            f"resource-in-nested-stack-{i}",
            resource_provider_service_token=resource_provider_service_token,
            resource_name=f"resource-{i}",
            version=version
          )
          
          if previous_nested_stack:
            nested_stack.add_dependency(previous_nested_stack)

          previous_nested_stack = nested_stack