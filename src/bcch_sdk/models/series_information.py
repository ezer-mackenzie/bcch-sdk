from pydantic import BaseModel

from datetime import date

from ..types.enums import Frequency


class SerieInformation(BaseModel):
    id: str
    frequency: Frequency
    spanish_title: str
    english_title: str
    first_observation: date
    last_observation: date
    updated_at: date
    created_at: date
