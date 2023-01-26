#!/usr/bin/env python3
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.insert(0, BASE_DIR)

import aws_cdk as cdk  # noqa: E402

from cdk.cdk.ecr_stack import EcrStack  # noqa: E402
from cdk.core import settings  # noqa: E402

app = cdk.App()
env = {
    'account': settings.CDK_ACCOUNT,
    'region': settings.CDK_REGION,
}

EcrStack(
    app,
    f'{settings.SERVICE_NAME}-ecr-stack',
    env=env,
)

app.synth()
