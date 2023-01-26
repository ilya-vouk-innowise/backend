import re
import typing
from functools import wraps
from inspect import signature
from typing import Any

from strawberry.types import Info

from app.core.db.db import async_session


class ValidationInputMixin:
    """Mixin for strawberry validation class. Defines _run_validation method to run all validators"""

    validators: dict[str, typing.Callable[[typing.Any], None]]

    def __init__(self, *args: tuple, **kwargs: Any):
        self._run_validation(data=kwargs)
        super().__init__(*args, **kwargs)

    def _run_validation(self, data: dict[str, typing.Any]) -> None:
        """Runs all schema validators"""
        for field, value in data.items():
            field_validators = self.validators.get(field, ())
            for validator in field_validators:  # type: ignore
                validator(value)


def inject_validation(cls: typing.Type) -> typing.Type:  # noqa
    """Injects the validators that is passed as a dict to the strawberry input schema"""

    class ValidationInput(ValidationInputMixin, cls):  # type: ignore
        pass

    return ValidationInput


def attrs_to_camel_case(string: str) -> str:
    """Convert snake_case string to camelCase string"""
    return re.sub('_.', lambda x: x.group()[1].capitalize(), string)


def attrs_to_snake_case(string: str) -> str:
    """Convert camelCase string to snake_case string"""
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def inject_session(func: typing.Callable) -> typing.Callable:
    """
    Injects the session that is passed as an argument to the mutation method
    """

    @wraps(func)
    async def wrapper(*args: tuple, **kwargs: Any) -> typing.Callable:
        async with async_session() as session:
            return await func(*args, session=session, **kwargs)

    func_signature = signature(func)
    params = dict(func_signature.parameters)
    del params['session']
    del wrapper.__annotations__['session']
    func_signature = func_signature.replace(
        parameters=params.values(),  # type: ignore
    )
    wrapper.__signature__ = func_signature  # type: ignore
    return wrapper
