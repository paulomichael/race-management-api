from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class RaceBase(BaseModel):
    name: str
    date: date
    location: str
    distance: float
    description: Optional[str] = None
    organizer_id: int

class RaceCreate(RaceBase):
    pass  # não tem campos extras

class RaceResponse(RaceBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
