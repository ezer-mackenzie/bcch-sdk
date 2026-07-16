from pydantic import BaseModel

from .observation_series import ObservationSeriesDTO


class SeriesDTO(BaseModel):
    seriesId: str
    descripEsp: str
    descripIng: str
    Obs: list[ObservationSeriesDTO]
