from typing import Optional

import awswrangler as wr

from app.core import settings
from app.core.elastic_apm import ElasticAPMLogger
from app.services.async_service import AsyncService

logger = ElasticAPMLogger(name=__name__)


class AthenaClient:
    """Client for handling Athena service with awswrangler"""

    @staticmethod
    async def read_sql_query(sql: str, params: Optional[dict] = None) -> list[dict]:
        """Execute any SQL query on AWS Athena and return the results as a Pandas DataFrame."""
        try:
            df = await AsyncService.async_function_call(
                function=wr.athena.read_sql_query,
                sql=sql,
                database=settings.ATHENA_DATABASE,
                params=params,
                use_threads=settings.ATHENA_THREADS_QUERY,
            )
        except wr.exceptions.QueryFailed as exc:
            logger.error(message=f'Query Failed: {exc=}')
            raise BaseException(f'Query Failed: {exc=}')
        except wr.exceptions.InvalidTable as exc:
            logger.error(message=f'Invalid Table: {exc=}')
            raise BaseException(f'Invalid Table: {exc=}')
        return df.to_dict('records')
