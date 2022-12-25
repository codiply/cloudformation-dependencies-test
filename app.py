#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.core_stack import CoreStack


prefix = "cfn-deps-test"

app = cdk.App()

core_stack = CoreStack(app, 
    f"{prefix}-core",
    prefix=prefix)

app.synth()
