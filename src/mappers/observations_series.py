from src.builders.date import DateBuilder

from src.models.observation_series import ObservationSeries

from src.dto.observation_series import ObservationSeriesDTO


class ObservationSeriesMapper:
    @classmethod
    def from_api_to_domain(cls, dto: ObservationSeriesDTO) -> ObservationSeries:
        return ObservationSeries(
            index_date=DateBuilder.to_date(dto.indexDateString),
            value=float(dto.value),
            status_code=dto.statusCode,
        )
