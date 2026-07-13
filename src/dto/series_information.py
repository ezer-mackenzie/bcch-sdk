from pydantic import BaseModel

from src.types.enums import Frequency

class SerieInformationDTO(BaseModel):
    seriesId: str
    frequencyCode: Frequency
    spanishTitle: str
    englishTitle: str
    firstObservation: str
    lastObservation: str
    updatedAt: str
    createdAt: str
