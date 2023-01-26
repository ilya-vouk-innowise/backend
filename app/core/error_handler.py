from botocore.exceptions import BotoCoreError
from fastapi import Request
from pydantic import ValidationError
from starlette import status
from starlette.responses import JSONResponse

from app.app import app
from app.core.exceptions.base_exception import (
    BadRequestError,
    ForbiddenError,
    UnauthorizedError,
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handles not valid data error"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': 'Provided values not valid.', 'metadata': f'{exc}'},
    )


@app.exception_handler(BadRequestError)
async def bad_request_error_handler(request: Request, exc: BadRequestError) -> JSONResponse:
    """Handles bad request error"""
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})


@app.exception_handler(ForbiddenError)
async def forbidden_error_handler(request: Request, exc: ForbiddenError) -> JSONResponse:
    """Handles forbidden error"""
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})


@app.exception_handler(UnauthorizedError)
async def unauthorized_error_handler(request: Request, exc: UnauthorizedError) -> JSONResponse:
    """Handles unauthorized error"""
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})


@app.exception_handler(BotoCoreError)
async def botocore_error_handler(request: Request, exc: BotoCoreError) -> JSONResponse:
    """Handles unexpected error from boto3"""
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={'detail': 'Unable to connect to the AWS'}
    )
