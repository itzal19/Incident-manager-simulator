from datetime import datetime, timedelta
from typing import List, Set, Optional
from incident.models import Incident

class Dispatcher:
    def __init__(self):
        self.incidents: List[Incident] = []
        self.id_counter: int = 1
        self.operators: Set[str] = {"Operator_1", "Operator_2", "Operator_3", "Operator_4"}
        self.history: List[str] = []
        self.escalation_minutes: int = 5

    def register_incident(self, incident_type: str, priority: str, description: str):
        incident = Incident(
            id=self.id_counter,
            type=incident_type,
            priority=priority,
            description=description
        )
        self.incidents.append(incident)
        print(f"Incident number {self.id_counter} registered.")
        self.id_counter += 1

    def show_pending_incidents(self):
        priority_order = {"high": 0, "medium": 1, "low": 2}
        pending_incidents = [inc for inc in self.incidents if inc.status == "pending"]
        pending_incidents.sort(key=lambda x: priority_order.get(x.priority, 3))

        if not pending_incidents:
            print("There are no pending incidents.")
            return

        print("Pending Incidents:")
        for inc in pending_incidents:
            print(f"[{inc.id}] {inc.type} | Priority: {inc.priority} | Status: {inc.status}")

    def assign_incident(self, incident_id: int, operator: str):
        incident = next((inc for inc in self.incidents if inc.id == incident_id), None)

        if not incident:
            print(f"Incident number {incident_id} not found.")
            return

        if incident.status != "pending":
            print(f"Incident number {incident_id} is not pending.")
            return

        if operator not in self.operators:
            print(f"'{operator}' not available.")
            return

        incident.assigned_to = operator
        print(f"Incident number {incident.id} assigned to {operator}.")

    def resolve_incident(self, incident_id: int):
        incident = next((inc for inc in self.incidents if inc.id == incident_id), None)

        if not incident:
            print(f"Incident number {incident_id} not found.")
            return

        if incident.status != "pending":
            print(f"Incident number {incident_id} cannot be resolved (status: {incident.status}).")
            return

        incident.status = "resolved"
        incident.resolved_at = datetime.now()
        self.history.append(f"Incident number {incident.id} resolved at {incident.resolved_at}")
        print(f"Incident #{incident.id} resolved.")

    def auto_escalate(self):
        now = datetime.now()
        for incident in self.incidents:
            if incident.status == "pending":
                diff = now - incident.created_at
                if diff > timedelta(minutes=self.escalation_minutes):
                    incident.status = "escalated"
                    self.history.append(f"Incident number {incident.id} escalated at {now}")
                    print(f"Incident number {incident.id} escalated automatically.")

    def show_history(self):
        if not self.history:
            print("No history yet.")
            return

        print("Incident History:")
        for record in self.history:
            print(record)