from pydantic import BaseModel

from src.models.observation_series import ObservationSeries

class Series(BaseModel):
    id: str
    spanish_description: str
    english_description: str
    observations: list[ObservationSeries]