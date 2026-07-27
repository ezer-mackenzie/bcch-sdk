from datetime import datetime, date

from ..exceptions import InvalidDateException

class DateBuilder:
    @staticmethod
    def to_string_date(value: str | datetime | date) -> str:
        if isinstance(value, (datetime, date)):
            return value.strftime("%Y-%m-%d")

        if not value.strip():
            raise InvalidDateException("Date string cannot be empty.")

        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value

        except ValueError:
            raise InvalidDateException(
                f"Invalid date format: '{value}'. Must be 'YYYY-MM-DD'."
            )

    @staticmethod
    def to_date(value: str) -> date:
        # The API always returns DD-MM-YYYY. This keeps calendar validation while
        # avoiding the generic and considerably slower strptime parser per row.
        if len(value) != 10 or value[2] != "-" or value[5] != "-":
            raise ValueError(f"time data {value!r} does not match format '%d-%m-%Y'")

        return date.fromisoformat(f"{value[6:10]}-{value[3:5]}-{value[0:2]}")
