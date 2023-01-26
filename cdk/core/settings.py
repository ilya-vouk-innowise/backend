import os

from dotenv import load_dotenv

from cdk.core.services.ecr_service import EcrService
from cdk.core.services.secrets_manager_service import SecretsManagerService

load_dotenv()


# others
PATH_TO_HEALTHCHECK = f'/{SERVICE_NAME}/api/health-check'
HEALTHCHECK_DURATION = os.getenv('HEALTHCHECK_DURATION', 120)  # in seconds
