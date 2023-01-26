import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.insert(
    0,
    BASE_DIR,
)


from cdk.core import settings  # noqa: E402
from cdk.core.services.ecr_service import EcrService  # noqa: E402
from cdk.core.services.secrets_manager_service import (  # noqa: E402
    SecretsManagerService,
)

if __name__ == '__main__':
    secrets = {}
    ecr_repository_uri = EcrService.get_repository_uri(
        account_id=settings.CDK_ACCOUNT,
        region_name=settings.AWS_DEFAULT_REGION,
        repository_name=settings.ECR_REPOSITORY_NAME,
    )
    secrets['ECR_REPOSITORY_URI'] = ecr_repository_uri

    SecretsManagerService.put_secrets(secrets_manager_name=settings.SECRETS_MANAGER_NAME, secrets=secrets)
