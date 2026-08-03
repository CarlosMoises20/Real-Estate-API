from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class ItemStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"


class ItemPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
    
class ItemCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=1000)
    priority: ItemPriority = ItemPriority.MEDIUM
    
    
class ItemUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    priority: Optional[ItemPriority] = None
    status: Optional[ItemStatus] = None


class ItemOut(BaseModel):
    id: str
    title: str
    description: str
    priority: ItemPriority
    status: ItemStatus