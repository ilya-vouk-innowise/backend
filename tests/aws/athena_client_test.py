import awswrangler as wr
import pandas as pd
import pytest
from pytest_mock import MockerFixture

from app.core.aws.athena_client import AthenaClient


class TestAthenaClient:
    SQL = 'CREATE TABLE test'

    @pytest.mark.asyncio
    async def test_read_sql_query(self, mocker: MockerFixture) -> None:
        mocker.patch('awswrangler.athena.read_sql_query', return_value=pd.DataFrame(data={'table': [1, 2]}))
        result = await AthenaClient.read_sql_query(sql=self.SQL)
        assert result == [{'table': 1}, {'table': 2}]

    @pytest.mark.asyncio
    async def test_read_sql_query_failed(self, mocker: MockerFixture) -> None:
        mocker.patch('awswrangler.athena.read_sql_query', side_effect=wr.exceptions.QueryFailed)
        with pytest.raises(BaseException):
            await AthenaClient.read_sql_query(sql=self.SQL)

    @pytest.mark.asyncio
    async def test_read_sql_query_invalid_table(self, mocker: MockerFixture) -> None:
        mocker.patch('awswrangler.athena.read_sql_query', side_effect=wr.exceptions.InvalidTable)
        with pytest.raises(BaseException):
            await AthenaClient.read_sql_query(sql=self.SQL)
