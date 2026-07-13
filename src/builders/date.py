from datetime import datetime, date

from src.exceptions import InvalidDateException

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
        return datetime.strptime(value, "%d-%m-%Y").date()