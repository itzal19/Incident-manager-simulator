from datetime import datetime, timedelta
import json
import re

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
        self.escalation_minutes = 5

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

    def auto_escalate(self):
        now = datetime.now()
        for incident in self.incidents:
            if incident.status == "pending":
                diff = now - incident.created_at
                if diff > timedelta(minutes=self.escalation_minutes):
                    # Solo escala si no está asignado o si ya está asignado pero no resuelto
                    incident.status = "escalated"
                    self.history.append(f"Incident number {incident.id} escalated at {now}")
                    print(f"Incident number {incident.id} escalated automatically.")

    def search_incidents(self):
        print("Search by 1:Text 2:Type 3:Operator 4:Date")
        choice = input("Choose option (1-4): ")

        if choice == "1":
            pattern = input("Enter text to search: ")
            #falta logica para buscar
        elif choice == "2":
            typ = input("Enter incident type: ")
            #falta logica para buscar
        elif choice == "3":
            name_op = input("Enter operator name: ")
            #falta logica para buscar
        elif choice == "4":
            try:
                start_date = input("Start date (dd/mm/yyyy): ")
                end_date = input("End date (dd/mm/yyyy): ")
                start = datetime.strptime(start_date, "%d/%m/%Y")
                end = datetime.strptime(end_date, "%d/%m/%Y")
                results = [inc for inc in self.incidents if start <= inc.created_at <= end]
            except ValueError:
                print("Invalid date format.")
                return
        else:
            print("Invalid option.")
            return

        if not results:
            print("No incidents found.")
            return

        for inc in results:
            print(f"[{inc.id}] {inc.type} | Priority: {inc.priority} | Status: {inc.status} | Assigned to: {inc.assigned_to}")
            #falta colocar tabla

    def save_to_json(self, filename="incidents.json"):
        data = []
        for inc in self.incidents:
            data.append({
                "id": inc.id,
                "type": inc.type,
                "priority": inc.priority,
                "description": inc.description,
                "created_at": inc.created_at,
                "assigned_to": inc.assigned_to,
                "status": inc.status,
                "resolved_at": inc.resolved_at if inc.resolved_at else None
            })
        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Incidents saved to {filename}.")
        except IOError as e:
            print(f"Error saving incidents: {e}")