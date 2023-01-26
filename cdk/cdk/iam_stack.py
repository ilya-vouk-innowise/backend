"""
AWS CDK Stack

https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html
https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html
"""
from typing import Any

from aws_cdk import Stack
from aws_cdk import aws_iam as iam
from constructs import Construct

from cdk.core import settings


class IamStack(Stack):
    """
    A stack is a collection of AWS resources.
    All the resources in a stack are defined by the stack's AWS CloudFormation template.
    This stack will responsible for creation IAm roles

    https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html
    https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_docdb/README.html
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)

        iam.Role(
            self,
            settings.CDK_STACK_CROSS_ACCOUNT_EC2_ROLE,
            role_name=settings.CROSS_ACCOUNT_EC2_ROLE_NAME,
            assumed_by=iam.ServicePrincipal(service='ec2.amazonaws.com'),
        )

        iam.Role(
            self,
            settings.CDK_STACK_CROSS_ACCOUNT_PIPELINE_ROLE,
            role_name=settings.CROSS_ACCOUNT_ROLE_NAME,
            assumed_by=iam.AccountPrincipal(account_id=settings.PIPELINE_ACCOUNT_ID),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")],
        )
