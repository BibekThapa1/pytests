from typing import Optional
from datetime import datetime

class DepartmentEntity:
    def __init__(
        self,
        name: str,
        content: str,
        id: Optional[int] = None,
        icon: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.content = content
        self.icon = icon
        self.created_at = created_at
        self.updated_at = updated_at