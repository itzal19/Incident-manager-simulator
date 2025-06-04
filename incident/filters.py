from typing import List, Optional
from incident.models import Incident

def filter_by_status(incidents: List[Incident], status: str) -> List[Incident]:
    return [inc for inc in incidents if inc.status == status]

def filter_by_priority(incidents: List[Incident], priority: str) -> List[Incident]:
    return [inc for inc in incidents if inc.priority == priority]

def filter_by_operator(incidents: List[Incident], operator: str) -> List[Incident]:
    return [inc for inc in incidents if inc.assigned_to == operator]

def get_pending_sorted_by_priority(incidents: List[Incident]) -> List[Incident]:
    priority_order = {"high": 0, "medium": 1, "low": 2}
    pending = filter_by_status(incidents, "pending")
    return sorted(pending, key=lambda inc: priority_order.get(inc.priority, 3))