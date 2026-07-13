from pydantic import BaseModel

from src.dto.observation_series import ObservationSeriesDTO


class SeriesDTO(BaseModel):
    seriesId: str
    descripEsp: str
    descripIng: str
    Obs: list[ObservationSeriesDTO]
