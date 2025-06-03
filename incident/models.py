from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass(slots=True)
class Incident:
    id: int
    type: str
    priority: str
    description: str
    created_at: datetime = field(default_factory=datetime.now)
    assigned_to: Optional[str] = None
    status: str = "pending"
    resolved_at: Optional[datetime] = None