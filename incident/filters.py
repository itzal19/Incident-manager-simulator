from typing import List, Optional
from incident.models import Incident

def filter_by_status(incidents: List[Incident], status: str) -> List[Incident]:
    return [inc for inc in incidents if inc.status == status]

def filter_by_priority(incidents: List[Incident], priority: str) -> List[Incident]:
    return [inc for inc in incidents if inc.priority == priority]

def filter_by_operator(incidents: List[Incident], operator: str) -> List[Incident]:
    return [inc for inc in incidents if inc.assigned_to == operator]