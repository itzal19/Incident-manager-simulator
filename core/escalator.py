from datetime import datetime, timedelta
from typing import List
from incident.models import Incident

class IncidentEscalator:
    def __init__(self, escalation_minutes: int = 5):
        self.escalation_minutes = escalation_minutes

    def auto_escalate(self, incidents: List[Incident], history: List[str]) -> None:
        now = datetime.now()
        for inc in incidents:
            if inc.status == "pending":
                diff = now - inc.created_at
                if diff > timedelta(minutes=self.escalation_minutes):
                    inc.status = "escalated"
                    history.append(f"Incidente {inc.id} escalado a las {now}")
                    print(f"Incidente {inc.id} escalado automáticamente.")