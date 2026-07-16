from abc import ABC
from abc import abstractmethod
from datetime import datetime, date

from ..models.web_service import WebServiceResponse

from ..types.enums import Frequency

from .base import BaseClient

class BaseAsyncClient(BaseClient, ABC):
    @abstractmethod
    async def get_series(
        self,
        time_series: str,
        first_date: str | date | datetime | None = None,
        last_date: str | date | datetime | None = None,
    ) -> WebServiceResponse: ...

    @abstractmethod
    async def search_series(self, frequency: Frequency) -> WebServiceResponse: ...
