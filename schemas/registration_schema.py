from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import time

class RegistrationBase(BaseModel):
    user_id: int
    race_id: int
    status: str = "inscrito"
    time: Optional[time] = None

class RegistrationCreate(RegistrationBase):
    pass

class RegistrationResponse(RegistrationBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
