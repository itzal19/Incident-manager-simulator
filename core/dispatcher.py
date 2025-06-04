from datetime import datetime
from typing import List, Set
from incident.models import Incident
from core.validator import IncidentValidator
from core.escalator import IncidentEscalator
from persistence.storage import save_history

class Dispatcher:
    def __init__(self):
        self.incidents: List[Incident] = []
        self.id_counter: int = 1
        self.operators = {
            "Carlos": {"profile": {"infraestructura", "seguridad"}, "busy": False},
            "Jairo": {"profile": {"aplicativo"}, "busy": False},
            "Jose": {"profile": {"infraestructura", "aplicativo"}, "busy": False},
            "Marco": {"profile": {"seguridad"}, "busy": False},
        }
        self.history: List[str] = []
        self.escalation_minutes: int = 1 #5
        self.escalator = IncidentEscalator(self.escalation_minutes)
        self.validator = IncidentValidator(self.incidents, self.operators)

    def register_incident(self, incident_type: str, priority: str, description: str):
        if not self.validator.validate_type(incident_type):
            print(f"Tipo inválido de incidente: '{incident_type}'.")
            return

        if not self.validator.validate_priority(priority):
            print(f"Prioridad inválida: '{priority}'.")
            return

        incident = Incident(
            id=self.id_counter,
            type=incident_type.lower(),
            priority=priority.lower(),
            description=description
        )

        priority_order = {"alta": 0, "media": 1, "baja": 2}
        inserted = False
        for idx, inc in enumerate(self.incidents):
            if priority_order[incident.priority] < priority_order[inc.priority]:
                self.incidents.insert(idx, incident)
                inserted = True
                break
        if not inserted:
            self.incidents.append(incident)

        print(f"✔ ID generado: {incident.id:03}")
        self.id_counter += 1

    def show_pending_incidents(self):
        self.auto_escalate()
        pending_incidents = [inc for inc in self.incidents if inc.status == "pending"]

        if not pending_incidents:
            print("No hay incidentes pendientes.")
            return

        print(f"> Ver incidentes pendientes ({len(pending_incidents)})")
        for inc in pending_incidents:
            print(f"[{inc.id:03}] {inc.type.capitalize()} | Prioridad: {inc.priority} | Estado: {inc.status}")

    def assign_incident(self, incident_id: int):
        incident = self.validator.incident_exists(incident_id)
        if not incident:
            print(f"Incidente {incident_id} no encontrado.")
            return

        if not self.validator.is_pending(incident):
            print(f"Incidente {incident_id} no está pendiente.")
            return

        for operator_name, data in self.operators.items():
            if not data["busy"] and incident.type in data["profile"]:
                incident.assigned_to = operator_name
                data["busy"] = True
                print(f"✔ Asignado correctamente a {operator_name}.")
                return

        print("No hay operadores disponibles con perfil compatible para este incidente.")

    def resolve_incident(self, incident_id: int):
        incident = self.validator.incident_exists(incident_id)

        if not incident:
            print(f"Incidente {incident_id} no encontrado.")
            return

        if not self.validator.is_pending(incident):
            print(f"Incidente {incident_id} no puede ser resuelto (estado: {incident.status}).")
            return

        incident.status = "resolved"
        incident.resolved_at = datetime.now()

        operator = incident.assigned_to
        if operator and operator in self.operators:
            self.operators[operator]["busy"] = False

        resolved_str = incident.resolved_at.strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{incident.id:03}] Incidente resuelto por {operator} a las {resolved_str}")
        save_history(self.history)
        print("✔ Marcado como resuelto")

    def auto_escalate(self):
        self.escalator.auto_escalate(self.incidents, self.history)

    def show_history(self):
        if not self.history:
            print("Aún no se cuenta con historial.")
            return

        print("> Ver historial")
        for record in self.history:
            print(record)