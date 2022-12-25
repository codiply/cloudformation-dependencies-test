#!/usr/bin/env python3

import aws_cdk as cdk

from stacks.core_stack import CoreStack
from stacks.no_dependency_stack import NoDependenciesStack


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

app.synth()
