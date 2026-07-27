from pydantic import BaseModel, ConfigDict, Field

from .observation_series import ObservationSeries


class Series(BaseModel):
    model_config = ConfigDict(validate_by_name=True)

    id: str = Field(validation_alias="seriesId")
    spanish_description: str = Field(validation_alias="descripEsp")
    english_description: str = Field(validation_alias="descripIng")
    observations: list[ObservationSeries] = Field(validation_alias="Obs")
