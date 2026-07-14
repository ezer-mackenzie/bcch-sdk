from src.mappers.series_information import SerieInformationMapper
from src.mappers.series import SeriesMapper

from src.models.web_service import WebServiceResponse
from src.models.series_information import SerieInformation
from src.models.series import Series

from src.dto.web_service import WebServiceResponseDTO


class WebServiceResponseMapper:
    @classmethod
    def from_api_to_domain(cls, dto: WebServiceResponseDTO) -> WebServiceResponse:
        series: Series | None = None
        series_information: list[SerieInformation] | None = None

        if dto.Series:
            series = SeriesMapper.from_api_to_domain(dto.Series)

        if dto.SeriesInfos:
            series_information = [
                SerieInformationMapper.from_api_to_domain(si) for si in dto.SeriesInfos
            ]

        return WebServiceResponse(
            code=dto.Codigo,
            description=dto.Descripcion,
            series=series,
            series_information=series_information,
        )
