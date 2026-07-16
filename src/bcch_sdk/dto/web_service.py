from pydantic import BaseModel

from .series import SeriesDTO
from .series_information import SerieInformationDTO


class WebServiceResponseDTO(BaseModel):
    Codigo: int
    Descripcion: str
    Series: SeriesDTO | None = None
    SeriesInfos: list[SerieInformationDTO] | None = None
