from pydantic import BaseModel

from src.models.series import Series
from src.models.series_information import SerieInformation


class WebServiceResponse(BaseModel):
    code: int
    description: str
    series: Series | None
    series_information: list[SerieInformation] | None
