from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.elastic_apm import ElasticAPMLogger


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = ElasticAPMLogger(name=__name__)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        self.logger.info(message=f'client:{request.client.host} - url:{request.url.path}')
        response = await call_next(request)
        return response
