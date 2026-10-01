from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import time

class ResultBase(BaseModel):
    race_id: int
    user_id: int
    position: int
    finish_time: Optional[time] = None

class ResultCreate(ResultBase):
    pass

class ResultResponse(ResultBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
