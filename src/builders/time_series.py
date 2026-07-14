from ..exceptions import InvalidSeriesException


class TimeSeriesBuilder:
    @staticmethod
    def to_list(time_series: str | list[str] | dict[str, str] | None) -> list[str]:
        if time_series is None or not time_series:
            raise InvalidSeriesException(
                "At least one series identifier must be provided."
            )

        if isinstance(time_series, str):
            return [serie for serie in time_series.replace(" ", "").split(",") if serie]

        if isinstance(time_series, dict):
            return [value for value in time_series.values() if value]

        return [serie for serie in time_series if serie]
