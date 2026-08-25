from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..builders.date import DateBuilder
from ..types.enums import Frequency


class SeriesInformation(BaseModel):
    model_config = ConfigDict(validate_by_name=True)

    id: str = Field(validation_alias="seriesId")
    frequency: Frequency = Field(validation_alias="frequencyCode")
    spanish_title: str = Field(validation_alias="spanishTitle")
    english_title: str = Field(validation_alias="englishTitle")
    first_observation: date = Field(validation_alias="firstObservation")
    last_observation: date = Field(validation_alias="lastObservation")
    updated_at: date = Field(validation_alias="updatedAt")
    created_at: date = Field(validation_alias="createdAt")

    @field_validator(
        "first_observation",
        "last_observation",
        "updated_at",
        "created_at",
        mode="before",
    )
    @classmethod
    def parse_api_date(cls, value: object) -> object:
        if isinstance(value, str) and len(value) == 10 and value[2] == "-":
            return DateBuilder.to_date(value)
        return value
