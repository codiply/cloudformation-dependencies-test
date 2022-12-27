#!/usr/bin/env python3

import aws_cdk as cdk

from stacks.core import CoreStack
from stacks.no_dependencies import NoDependenciesStack
from stacks.with_dependencies import WithDependenciesStack
from stacks.with_nested_stacks import NestedStacksWithDependenciesStack


PREFIX = "cfn-deps-test"
NUMBER_OF_RESOURCES=10
VERSION = "1"

app = cdk.App()

core_stack = CoreStack(
    app, 
    f"{PREFIX}-core",
    prefix=PREFIX)

NoDependenciesStack(
    app,
    f"{PREFIX}-no-dependencies",
    resource_provider_service_token=core_stack.resource_provider_service_token,
    number_of_resources=NUMBER_OF_RESOURCES,
    version=VERSION)

WithDependenciesStack(
    app,
    f"{PREFIX}-with-dependencies",
    resource_provider_service_token=core_stack.resource_provider_service_token,
    number_of_resources=NUMBER_OF_RESOURCES,
    version=VERSION)

NestedStacksWithDependenciesStack(
    app,
    f"{PREFIX}-with-nested-stacks",
    resource_provider_service_token=core_stack.resource_provider_service_token,
    number_of_resources=NUMBER_OF_RESOURCES,
    version=VERSION)


app.synth()
