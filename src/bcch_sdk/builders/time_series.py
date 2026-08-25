from ..exceptions import InvalidSeriesException


class TimeSeriesBuilder:
    @staticmethod
    def to_list(time_series: str | list[str] | dict[str, str] | None) -> list[str]:
        if not time_series:
            raise InvalidSeriesException(
                "At least one series identifier must be provided."
            )

        if isinstance(time_series, str):
            candidates = time_series.split(",")
        elif isinstance(time_series, dict):
            candidates = list(time_series.values())
        elif isinstance(time_series, list):
            candidates = time_series
        else:
            raise InvalidSeriesException(
                "Series identifiers must be a string, list, or dictionary."
            )

        if any(not isinstance(value, str) for value in candidates):
            raise InvalidSeriesException("Every series identifier must be a string.")

        series = list(
            dict.fromkeys(value.strip() for value in candidates if value.strip())
        )
        if not series:
            raise InvalidSeriesException(
                "At least one non-empty series identifier must be provided."
            )

        return series
