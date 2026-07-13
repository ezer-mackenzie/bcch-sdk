from pydantic import BaseModel

class ObservationSeriesDTO(BaseModel):
    indexDateString: str
    value: str
    statusCode: str