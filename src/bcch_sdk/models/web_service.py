from pydantic import BaseModel, ConfigDict, Field

from .series import Series
from .series_information import SeriesInformation


class WebServiceResponse(BaseModel):
    model_config = ConfigDict(validate_by_name=True)

    code: int = Field(validation_alias="Codigo")
    description: str = Field(validation_alias="Descripcion")
    series: Series | None = Field(default=None, validation_alias="Series")
    series_information: list[SeriesInformation] | None = Field(
        default=None,
        validation_alias="SeriesInfos",
    )
