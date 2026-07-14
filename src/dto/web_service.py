from pydantic import BaseModel

from ..dto.series import SeriesDTO
from ..dto.series_information import SerieInformationDTO

class WebServiceResponseDTO(BaseModel):
    Codigo: int
    Descripcion: str
    Series: SeriesDTO
    SeriesInfos: list[SerieInformationDTO]
    
    