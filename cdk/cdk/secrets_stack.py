"""
AWS CDK Stack

https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html
https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html
"""
from typing import Any

from aws_cdk import Stack
from aws_cdk import aws_secretsmanager as secrets_manager
from constructs import Construct

from cdk.core import settings


class SecretsStack(Stack):
    """
    A stack is a collection of AWS resources.
    All the resources in a stack are defined by the stack's AWS CloudFormation template.
    This stack will responsible for creation of Secrets Manager

    https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html
    https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_secretsmanager/Secret.html
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)

        secrets_manager.Secret(
            self,
            settings.SECRETS_MANAGER_CONSTRUCT_ID,
            secret_name=settings.SECRETS_MANAGER_NAME,
        )
