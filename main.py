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

class IncidentManager:
    def __init__(self):
        self.incidents = []
        self.id_counter = 1

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
        pending_incidents.sort(key=lambda inc: priority_order.get(inc.priority, 3))

        if not pending_incidents:
            print("There are not pending incidents.")
            return

        print("Pending incidents:")
        for i in pending_incidents:
            print(f"[{i.id}] {i.type} | Priority: {i.priority} | Status: {i.status}")