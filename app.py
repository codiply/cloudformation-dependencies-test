#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.timestream_stack import TimestreamStack


prefix = "cfn-deps-test"

app = cdk.App()
TimestreamStack(app, 
    f"{prefix}-timestream",
    prefix=prefix)

app.synth()
