from pydantic import BaseModel

from .series import Series
from .series_information import SeriesInformation


class WebServiceResponse(BaseModel):
    code: int
    description: str
    series: Series | None
    series_information: list[SeriesInformation] | None
