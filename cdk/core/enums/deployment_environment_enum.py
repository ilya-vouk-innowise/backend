from enum import Enum


class DeploymentEnvironmentEnum(Enum):
    DEV = 'development'
    STAGE = 'staging'
    PROD = 'production'
