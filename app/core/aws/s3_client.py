from app.core import settings
from app.core.aws.base_client import ClientMeta
from app.core.elastic_apm import ElasticAPMLogger
from app.services.async_service import AsyncService

logger = ElasticAPMLogger(name=__name__)


class S3Client(metaclass=ClientMeta):
    """Client for handling S3 service with boto3"""

    _client = None
    _service_name = 's3'

    @classmethod
    async def check_file_exist(cls, s3_key: str) -> tuple[bool, str]:
        try:
            result = await AsyncService.async_function_call(
                function=cls.client.list_objects_v2, Bucket=settings.S3_ATHENA_TABLE_BUCKET_NAME, Prefix=s3_key
            )
            return bool(result.get('Contents')), result.get('Prefix')
        except cls.client.exceptions.NoSuchBucket:
            logger.error(
                message=f'No such bucket: {settings.S3_ATHENA_TABLE_BUCKET_NAME}',
            )
            raise cls.client.exceptions.NoSuchBucket(detail=f'No such bucket: {settings.S3_ATHENA_TABLE_BUCKET_NAME}')
