import pytest
from botocore.exceptions import BotoCoreError
from fastapi import Request, status
from pydantic import ValidationError

from app.core.error_handler import (
    bad_request_error_handler,
    botocore_error_handler,
    forbidden_error_handler,
    unauthorized_error_handler,
    validation_exception_handler,
)
from app.core.exceptions.base_exception import (
    BadRequestError,
    ForbiddenError,
    UnauthorizedError,
)


class TestErrorHandler:
    @pytest.mark.asyncio
    async def test_validation_exception_handler(self) -> None:
        response = await validation_exception_handler(request=Request, exc=ValidationError)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_bad_request_error_handler(self) -> None:
        response = await bad_request_error_handler(request=Request, exc=BadRequestError())
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    async def test_forbidden_error_handler(self) -> None:
        response = await forbidden_error_handler(request=Request, exc=ForbiddenError())
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    async def test_unauthorized_error_handler(self) -> None:
        response = await unauthorized_error_handler(request=Request, exc=UnauthorizedError())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_botocore_error_handler(self) -> None:
        response = await botocore_error_handler(request=Request, exc=BotoCoreError)
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
