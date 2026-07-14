from pydantic import BaseModel

from src.dto.series import SeriesDTO
from src.dto.series_information import SerieInformationDTO

class WebServiceResponseDTO(BaseModel):
    Codigo: int
    Descripcion: str
    Series: SeriesDTO
    SeriesInfos: list[SerieInformationDTO]
    
    