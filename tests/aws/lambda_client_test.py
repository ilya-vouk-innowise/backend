import pytest
from pytest_mock import MockerFixture

from app.core.aws.lambda_client import LambdaClient
from tests.mocks import Mocks


class TestLambdaClient:
    @pytest.mark.asyncio
    async def test_trigger_lambda_function(self, mocker: MockerFixture) -> None:
        Mocks.mock_lambda_call(mocker=mocker, return_value={})
        assert await LambdaClient().trigger_lambda_function(event={}) == {}

    @pytest.mark.asyncio
    async def test_trigger_lambda_function_connection_error(self, mocker: MockerFixture) -> None:
        Mocks.mock_lambda_call_connection_error(mocker=mocker)
        with pytest.raises(ConnectionError):
            await LambdaClient().trigger_lambda_function(event={})
