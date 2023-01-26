from starlette import status


class BaseError(Exception):
    status_code: int
    default_detail: str

    def __init__(self, detail: str = None):
        self.detail = detail or self.default_detail


class BadRequestError(BaseError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'The server cannot process the request from the client'


class ValidationError(Exception):
    pass


class ForbiddenError(BaseError):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Forbidden'


class UnauthorizedError(BaseError):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Unauthorized'


class NotFoundError(Exception):
    pass
