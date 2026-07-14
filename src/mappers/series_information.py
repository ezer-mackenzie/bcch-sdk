from ..builders.date import DateBuilder

from ..dto.series_information import SerieInformationDTO

from ..models.series_information import SerieInformation


class SerieInformationMapper:
    @staticmethod
    def from_api_to_domain(dto: SerieInformationDTO) -> SerieInformation:
        return SerieInformation(
            id=dto.seriesId,
            frequency=dto.frequencyCode,
            spanish_title=dto.spanishTitle,
            english_title=dto.englishTitle,
            first_observation=DateBuilder.to_date(dto.firstObservation),
            last_observation=DateBuilder.to_date(dto.lastObservation),
            updated_at=DateBuilder.to_date(dto.updatedAt),
            created_at=DateBuilder.to_date(dto.createdAt),
        )
