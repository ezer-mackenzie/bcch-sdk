from .observations_series import ObservationSeriesMapper

from ..models.series import Series

from ..dto.series import SeriesDTO


class SeriesMapper:
    @staticmethod
    def from_api_to_domain(dto: SeriesDTO) -> Series:
        observations = [ObservationSeriesMapper.from_api_to_domain(o) for o in dto.Obs]

        return Series(
            id=dto.seriesId,
            spanish_description=dto.descripEsp,
            english_description=dto.descripIng,
            observations=observations,
        )
