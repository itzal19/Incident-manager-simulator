from datetime import datetime

class Incident:
    def __init__(self, id, incident_type, priority, description):
        self.id = id
        self.type = incident_type
        self.priority = priority
        self.description = description
        self.created_at = datetime.now()
        self.assigned_to = None
        self.status = "pending"
        self.resolved_at = None

class IncidentManager:
    def __init__(self):
        self.incidents = []
        self.id_counter = 1
        self.operators = {"Operator_1", "Operator_2", "Operator_3", "Operator_4"}
        self.history = []

    def register_incident(self):
        incident_type = input("Type (e.g., infrastructure, security, application): ")
        priority = input("Priority (high, medium, low): ")
        description = input("Description: ")

        incident = Incident(
            id=self.id_counter,
            incident_type=incident_type,
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
            print("There are not pending incidents.")
            return

        print("Pending Incidents:")
        for i in pending_incidents:
            print(f"[{i.id}] {i.type} | Priority: {i.priority} | Status: {i.status}")

    def assign_incident(self):
        incident_id = int(input("Enter incident ID to assign: "))
        incident = next((inc for inc in self.incidents if inc.id == incident_id), None)
        if not incident:
            print(f"Incident number {incident_id} not found.")
            return

        if incident.status != "pending":
            print(f"Incident number {incident_id} is not pending.")
            return

        print(f"Available operators: {', '.join(self.operators)}")
        operator = input("Assign to operator: ")

        if operator not in self.operators:
            print(f"Operator '{operator}' not available.")
            return

        incident.assigned_to = operator
        print(f"Incident number {incident.id} assigned to {operator}.")

    def resolve_incident(self):
        incident_id = int(input("Enter incident ID to resolve: "))
        incident = None

        for inc in self.incidents:
            if inc.id == incident_id:
                incident = inc
                break 

        if not incident:
            print(f"Incident #{incident_id} not found.")
            return

        if incident.status != "pending":
            print(f"Incident number {incident_id} cannot be resolved (status: {incident.status}).")
            return

        incident.status = "resolved"
        incident.resolved_at = datetime.now()
        self.history.append(f"Incident number {incident.id} resolved at {incident.resolved_at}")
        print(f"Incident number {incident.id} resolved.")

    def show_history(self):
        if not self.history:
            print("No history yet.")
            return

        print("Incident History:")
        for record in self.history:
            print(record)