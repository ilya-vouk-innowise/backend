import pytest
from botocore.client import BaseClient

from app.core import settings
from app.core.aws.s3_client import S3Client


class TestS3Client:
    async def test_check_file_exist(self, s3_client: BaseClient) -> None:
        S3Client._client = s3_client
        result = await S3Client.check_file_exist(s3_key='s3_key')
        assert not result[0]

    async def test_check_file_exist_no_such_bucket(self, s3_client: BaseClient) -> None:
        S3Client._client = s3_client
        s3_client.delete_bucket(Bucket=settings.S3_ATHENA_TABLE_BUCKET_NAME)
        with pytest.raises(Exception):
            await S3Client.check_file_exist(s3_key=settings.S3_ATHENA_TABLE_BUCKET_NAME)
