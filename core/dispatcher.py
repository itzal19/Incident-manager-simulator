from datetime import datetime, timedelta
from typing import List, Set, Optional
from incident.models import Incident
from core.validator import IncidentValidator
from incident.filters import get_pending_sorted_by_priority

class Dispatcher:
    def __init__(self):
        self.incidents: List[Incident] = []
        self.id_counter: int = 1
        self.operators: Set[str] = {"Operator_1", "Operator_2", "Operator_3", "Operator_4"}
        self.history: List[str] = []
        self.escalation_minutes: int = 5

    def register_incident(self, incident_type: str, priority: str, description: str):
        if not IncidentValidator.validate_type(incident_type):
            print(f"Invalid incident type: '{incident_type}'.")
            return

        if not IncidentValidator.validate_priority(priority):
            print(f"Invalid priority: '{priority}'.")
            return

        incident = Incident(
            id=self.id_counter,
            type=incident_type.lower(),
            priority=priority.lower(),
            description=description
        )

        self.incidents.append(incident)
        print(f"Incident number {self.id_counter} registered.")
        self.id_counter += 1

    def show_pending_incidents(self):
        pending_incidents = get_pending_sorted_by_priority(self.incidents)

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

        if not IncidentValidator.validate_operator(operator, self.operators):
            print(f"'{operator}' not available.")
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
        print(f"Incident number {incident.id} resolved.")

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