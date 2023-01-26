#!/usr/bin/env python3
import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.insert(0, BASE_DIR)

import aws_cdk as cdk  # noqa: E402
from cdk.core import settings  # noqa: E402

from cdk.cdk.cdk_stack import CdkStack  # noqa: E402
from cdk.cdk.ecr_stack import EcrStack  # noqa: E402
from cdk.cdk.pipeline_stack import PipelineStack  # noqa: E402
from cdk.cdk.secrets_stack import SecretsStack  # noqa: E402


logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s - %(name)s - %(message)s')

app = cdk.App()
env = {
    'account': settings.CDK_ACCOUNT,
    'region': settings.CDK_REGION,
}

SecretsStack(
    app,
    f'{settings.SERVICE_NAME}-secrets-stack',
    env=env,
)

EcrStack(
    app,
    f'{settings.SERVICE_NAME}-ecr-stack',
    env=env,
)

PipelineStack(
    app,
    f'{settings.SERVICE_NAME}-pipeline-stack',
    env=env,
)

CdkStack(
    app,
    f'{settings.SERVICE_NAME}-cdk-stack',
    env={
        'account': settings.CDK_ACCOUNT,
        'region': settings.CDK_REGION,
    },
)

app.synth()
