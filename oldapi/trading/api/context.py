#from __future__ import annotations # Dont touch, this causes a pydantic bug

from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from fastapi import Request

if TYPE_CHECKING:
    from trading.adapters.mysql import MySQLService


class Context(ABC):
    @property
    @abstractmethod
    def mysql(self) -> "MySQLService":
        ...

    @property
    @abstractmethod
    def request(self) -> "Request":
        ...


class HTTPContext(Context):
    def __init__(self, request: Request) -> None:
        self._request = request

    @property
    def request(self) -> "Request":
        return self._request
    
    @property
    def mysql(self) -> "MySQLService":
        return self._request.state.mysql
