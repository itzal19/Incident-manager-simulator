from datetime import datetime
from typing import List, Set, Optional
from incident.models import Incident

class IncidentValidator:
    valid_types = {"infraestructura", "seguridad", "aplicativo"}
    valid_priorities = {"alta", "media", "baja"}

    def __init__(self, incidents: List[Incident], operators: dict):
        self.incidents = incidents
        self.operators = operators

    @staticmethod
    def validate_type(incident_type: str) -> bool:
        return incident_type.lower() in IncidentValidator.valid_types

    @staticmethod
    def validate_priority(priority: str) -> bool:
        return priority.lower() in IncidentValidator.valid_priorities

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
    
    def incident_exists(self, incident_id: int) -> Optional[Incident]:
        return next((inc for inc in self.incidents if inc.id == incident_id), None)

    def is_pending(self, incident: Incident) -> bool:
        return incident.status == "pending"

    def is_valid_operator(self, operator: str) -> bool:
        return operator in self.operators

    def operator_can_handle_type(self, operator: str, incident_type: str) -> bool:
        if operator not in self.operators:
            return False
        return incident_type in self.operators[operator]["profile"]