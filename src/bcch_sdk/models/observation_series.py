from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..builders.date import DateBuilder


class ObservationSeries(BaseModel):
    model_config = ConfigDict(validate_by_name=True)

    index_date: date = Field(validation_alias="indexDateString")
    value: float
    status_code: str = Field(validation_alias="statusCode")

    @field_validator("index_date", mode="before")
    @classmethod
    def parse_api_date(cls, value: object) -> object:
        if isinstance(value, str) and len(value) == 10 and value[2] == "-":
            return DateBuilder.to_date(value)
        return value
