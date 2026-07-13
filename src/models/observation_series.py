from pydantic import BaseModel

from datetime import date

class ObservationSeries(BaseModel):
    index_date: date
    value: float
    status_code: str