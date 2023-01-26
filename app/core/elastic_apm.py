import logging
from datetime import datetime

from elasticapm.contrib.starlette import make_apm_client

from app.core import settings
from app.core.enums.logs_enum import LogLevelEnum

apm_config = {
    'SERVICE_NAME': settings.APM_SERVICE_NAME,
    'SERVER_URL': settings.APM_SERVER_URL,
    'ENVIRONMENT': settings.APM_ENVIRONMENT,
    'SECRET_TOKEN': settings.APM_SECRET_TOKEN,
}

apm_client = make_apm_client(apm_config)


class ElasticAPMLogger:
    """Creates Elastic APM logger"""

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)

    def capture_logs(self, level: str, message: str) -> None:
        """Basic method to send logs to Elastic APM and display it in the console"""
        getattr(self.logger, level.lower())(message)
        apm_client.capture_message(f'{level}: {datetime.now()} - {self.name} - {message}', level=level.lower())

    def info(self, message: str) -> None:
        """Send Info logs to Elastic APM and display it in console"""
        self.capture_logs(level=LogLevelEnum.INFO.value, message=message)

    def error(self, message: str) -> None:
        """Send Error logs to Elastic APM and display it in console"""
        self.capture_logs(level=LogLevelEnum.ERROR.value, message=message)

    def warning(self, message: str) -> None:
        """Send Warning logs to Elastic APM and display it in console"""
        self.capture_logs(level=LogLevelEnum.WARNING.value, message=message)
