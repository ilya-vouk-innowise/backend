"""
AWS CDK Stack

https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html
https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html
"""
from typing import Any

from aws_cdk import Stack
from aws_cdk import aws_ecr as ecr
from constructs import Construct

from cdk.core import settings


class EcrStack(Stack):
    """
    A stack is a collection of AWS resources.
    All the resources in a stack are defined by the stack's AWS CloudFormation template.
    This stack will responsible for creation of ECR repository

    https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html
    https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_ecr/Repository.html
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ecr.Repository(self, settings.ECR_REPOSITORY_CONSTRUCT_ID, repository_name=settings.ECR_REPOSITORY_NAME)
