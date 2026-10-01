from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "corredor"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    profile_picture: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
