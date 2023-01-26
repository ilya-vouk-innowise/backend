import json

import botocore.exceptions

from app.core import settings
from app.core.aws.base_client import ClientMeta
from app.core.elastic_apm import ElasticAPMLogger
from app.services.async_service import AsyncService

logger = ElasticAPMLogger(name=__name__)


class LambdaClient(metaclass=ClientMeta):
    """Client for handling lambda functions with boto3"""

    _client = None
    _service_name = 'lambda'

    @classmethod
    async def trigger_lambda_function(cls, event: dict) -> dict:
        """Async lambda function call"""
        try:
            return await AsyncService.async_function_call(
                function=cls.client.invoke,
                FunctionName=settings.LAMBDA_FUNCTION_GKLKL_PROCESS,
                Payload=json.dumps(event),
            )
        except botocore.exceptions.ClientError as ex:
            logger.error(message=f'Trigger lambda function error: {ex}')
            raise ConnectionError
