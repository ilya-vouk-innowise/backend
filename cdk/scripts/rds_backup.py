import argparse
import os
import sys
import uuid

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

sys.path.insert(
    0,
    BASE_DIR,
)

from cdk.core import settings  # noqa: E402
from cdk.core.services.ecs_service import EcsService  # noqa: E402
from cdk.core.services.rds_service import RdsService  # noqa: E402
from cdk.core.services.secrets_manager_service import (  # noqa: E402
    SecretsManagerService,
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name_snapshot', type=str, help='Input snapshot name')
    snapshots_identifier = parser.parse_args().name_snapshot

    db_instance_identifier = uuid.uuid4().hex

    db_instance = RdsService.create_db_backup(
        snapshots_identifier=snapshots_identifier, db_instance_identifier=db_instance_identifier
    )
    secrets = {
        'POSTGRES_HOST': db_instance['Endpoint']['Address'],
        'POSTGRES_INSTANCE_IDENTIFIER': db_instance['DBInstanceIdentifier'],
    }
    SecretsManagerService.put_secrets(secrets_manager_name=settings.SECRETS_MANAGER_NAME, secrets=secrets)
    EcsService.stop_all_ecs_tasks()
