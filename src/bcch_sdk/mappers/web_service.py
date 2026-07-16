from .series_information import SerieInformationMapper
from .series import SeriesMapper

from ..models.web_service import WebServiceResponse
from ..models.series_information import SeriesInformation
from ..models.series import Series

from ..dto.web_service import WebServiceResponseDTO


class WebServiceResponseMapper:
    @classmethod
    def from_api_to_domain(cls, dto: WebServiceResponseDTO) -> WebServiceResponse:
        series: Series | None = None
        series_information: list[SeriesInformation] | None = None

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
