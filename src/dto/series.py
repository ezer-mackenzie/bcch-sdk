from pydantic import BaseModel

from ..dto.observation_series import ObservationSeriesDTO


class SeriesDTO(BaseModel):
    seriesId: str
    descripEsp: str
    descripIng: str
    Obs: list[ObservationSeriesDTO]
