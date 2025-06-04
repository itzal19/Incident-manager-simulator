from typing import Set
from datetime import datetime

class IncidentValidator:
    valid_types = {"infrastructure", "security", "application"}
    valid_priorities = {"high", "medium", "low"}

    @staticmethod
    def validate_type(incident_type: str) -> bool:
        return incident_type.lower() in IncidentValidator.valid_types

    @staticmethod
    def validate_priority(priority: str) -> bool:
        return priority.lower() in IncidentValidator.valid_priorities

    @staticmethod
    def validate_operator(operator: str, available_operators: Set[str]) -> bool:
        return operator in available_operators

    @staticmethod
    def validate_date_format(date_str: str) -> bool:
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        return datetime.strptime(date_str, "%d/%m/%Y")