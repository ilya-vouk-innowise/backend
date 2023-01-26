import base64
from json import JSONDecodeError
from typing import Union

import httpx

from app.core import settings
from app.core.aws.base_client import ClientMeta
from app.core.elastic_apm import ElasticAPMLogger
from app.services.async_service import AsyncService

logger = ElasticAPMLogger(name=__name__)


class MWAAClient(metaclass=ClientMeta):
    """Client for handling lambda functions with boto3"""

    _client = None
    _service_name = 'mwaa'

    @classmethod
    async def get_dag_state(cls, dag_id: str, dag_execution_date: str) -> str:
        """Returns string with dag run status from MWAA"""
        return await AsyncService.async_function_call(
            function=cls._execute, payload=f'dags state {dag_id} {dag_execution_date}'
        )

    @classmethod
    def _get_mwaa_cli_token(cls, mwaa_env_name: str) -> Union[dict, None]:
        """Creates and returns mwaa cli token"""
        try:
            cli_token = cls.client.create_cli_token(Name=mwaa_env_name)
            logger.info(message='Cli token created successfully')
            return cli_token
        except cls.client.exceptions.ResourceNotFoundException:
            logger.error(message=f'Environment {mwaa_env_name} not found')

    @classmethod
    def _execute(cls, payload: str) -> str:
        """
        Generate cli token and make request to the MWAA service with payload.
        Receives and decodes the response.
        Returns decoded string response.
        """
        mwaa_response = ''
        cli_token = cls._get_mwaa_cli_token(mwaa_env_name=settings.MWAA_ENV_NAME)
        headers = {'Authorization': f'Bearer {cli_token["CliToken"]}', 'Content-Type': 'text/plain'}

        with httpx.Client() as client:
            response = client.post(
                url=f'https://{cli_token["WebServerHostname"]}/aws_mwaa/cli', headers=headers, content=payload
            )

        try:
            decoded_response = response.json()
            mwaa_response = base64.b64decode(decoded_response["stdout"]).decode("UTF-8")
            logger.info(message=mwaa_response)
        except JSONDecodeError as ex:
            logger.error(message=f'Error during decoding MWAA response: {ex}.\nThe MWAA response is: {response}')
        return mwaa_response
