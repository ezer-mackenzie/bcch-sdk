from pydantic import BaseModel

from .series import Series
from .series_information import SerieInformation


class WebServiceResponse(BaseModel):
    code: int
    description: str
    series: Series | None
    series_information: list[SerieInformation] | None
