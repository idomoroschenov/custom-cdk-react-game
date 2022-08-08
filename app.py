#!/usr/bin/env python3
import os

import aws_cdk as cdk

from custom_cdk_react_game.custom_cdk_react_game_stack import PipelineStack


app = cdk.App()
PipelineStack(app, "CustomCdkReactGameStack")

app.synth()
