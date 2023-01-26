import boto3
from botocore.client import BaseClient


class ClientMeta(type):
    """This is a base client for all AWS services"""

    @property
    def client(cls) -> BaseClient:
        """
        Returns a low-level service client by name
        using the default session.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/boto3.html
        https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3.html#client

        Return:
            service client instance
        """
        if not getattr(cls, '_client', None):
            service_name = getattr(cls, '_service_name')
            client = boto3.client(service_name)
            setattr(cls, '_client', client)
        return getattr(cls, '_client')
