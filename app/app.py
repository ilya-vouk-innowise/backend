import logging

import uvicorn
from codecovopentelem import CoverageSpanFilter, get_codecov_opentelemetry_instances
from elasticapm.contrib.starlette import ElasticAPM
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

from app.core import settings
from app.core.elastic_apm import apm_client
from app.core.middleware.logging_middleware import LoggingMiddleware
from app.rest.api.router import router as api_router

provider = TracerProvider()
trace.set_tracer_provider(provider)

generator, exporter = get_codecov_opentelemetry_instances(
    repository_token=settings.CODECOV_TOKEN_IMPACT,
    version_identifier=settings.CODECOV_VERSION,
    sample_rate=1,
    filters={
        CoverageSpanFilter.regex_name_filter: None,
        CoverageSpanFilter.span_kind_filter: [
            trace.SpanKind.SERVER,
            trace.SpanKind.CONSUMER,
        ],
    },
    code=f'{settings.CODECOV_VERSION}:{settings.CODECOV_ENV}',
    untracked_export_rate=0,
    environment=settings.CODECOV_ENV,
)
provider.add_span_processor(generator)
provider.add_span_processor(BatchSpanProcessor(exporter))
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=settings.CORS_ALLOWED_HEADERS,
    ),
    Middleware(
        LoggingMiddleware,
    ),
    Middleware(ElasticAPM, client=apm_client),
]

app = FastAPI(
    middleware=middlewares,
    openapi_url=f'/{settings.ENDPOINTS_SERVICE_PREFIX}/api/openapi.json',
    docs_url=f'/{settings.ENDPOINTS_SERVICE_PREFIX}/api/docs',
    redoc_url=f'/{settings.ENDPOINTS_SERVICE_PREFIX}/api/redoc',
)
if settings.TEST_ENVIRONMENT:
    FastAPIInstrumentor().instrument_app(app)

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(asctime)s - %(name)s - %(message)s')

app.include_router(api_router, prefix=f'/{settings.ENDPOINTS_SERVICE_PREFIX}/api')

from app.core import error_handler, settings  # noqa

if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, host='0.0.0.0', port=82)
