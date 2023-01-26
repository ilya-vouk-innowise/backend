import base64
from unittest.mock import Mock

from _pytest.logging import LogCaptureFixture
from pytest_mock import MockerFixture
from requests import Response

from app.core.aws.mwaa_client import MWAAClient


class TestMWAAClient:
    @staticmethod
    def mock_mwaa_get_token(mocker: MockerFixture, return_value: str) -> None:
        mocker.patch('app.core.aws.mwaa_client.MWAAClient.client.create_cli_token', new=Mock(return_value=return_value))

    @staticmethod
    def mock_mwaa_execute(mocker: MockerFixture, return_value: str) -> None:
        mocker.patch('app.core.aws.mwaa_client.MWAAClient._execute', new=Mock(return_value=return_value))

    def test_execute(self, mocker: MockerFixture):
        response = Response()
        status = '{"status": "SUCCESS"}'
        stdout = base64.b64encode(status.encode('UTF-8')).decode('UTF-8')
        response._content = bytes(f'{{"stdout": "{stdout}"}}', 'UTF-8')
        payload = 'dags state dag_id dag_execution_date'
        mocker.patch(
            'app.core.aws.mwaa_client.MWAAClient._get_mwaa_cli_token',
            new=Mock(return_value={'CliToken': 'test_token', 'WebServerHostname': 'test_host'}),
        )
        mocker.patch('httpx._client.Client.post', new=Mock(return_value=response))
        actual_result = MWAAClient._execute(payload=payload)
        assert actual_result == status

    def test_get_mwaa_cli_token(self, mocker: MockerFixture) -> None:
        expected_result = 'expected'
        self.mock_mwaa_get_token(mocker=mocker, return_value=expected_result)
        actual_result = MWAAClient._get_mwaa_cli_token(mwaa_env_name='fake')
        assert actual_result == expected_result

    async def test_get_dag_state(self, mocker: MockerFixture) -> None:
        expected_result = 'fake_response'
        self.mock_mwaa_execute(mocker=mocker, return_value=expected_result)
        actual_result = await MWAAClient.get_dag_state(dag_id='fake', dag_execution_date='fake')
        assert actual_result == expected_result

    def test_execute_failed(self, mocker: MockerFixture, caplog: LogCaptureFixture) -> None:
        response = Response()
        payload = 'dags state dag_id dag_execution_date'
        mocker.patch(
            'app.core.aws.mwaa_client.MWAAClient._get_mwaa_cli_token',
            new=Mock(return_value={'CliToken': 'test_token', 'WebServerHostname': 'test_host'}),
        )
        mocker.patch('httpx._client.Client.post', new=Mock(return_value=response))
        MWAAClient._execute(payload=payload)
        assert 'Error during decoding MWAA' == caplog.records[0].message[0:26]
