from typing import List, Optional
from enum import Enum
from sqlmodel import SQLModel, Field, JSON, Column

class UserStatus(str, Enum):
    individual = "individual"
    professional = "professional"

class ActivityType(str, Enum):
    rental = "rental"
    guide = "guide"

class UserBase(SQLModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    birthDate: Optional[str] = None # Keeping as string for simplicity, could be date
    email: str = Field(index=True, unique=True)
    phone: Optional[str] = None
    address: Optional[str] = None
    postalCode: Optional[str] = None
    city: Optional[str] = None
    avatarUrl: Optional[str] = None
    languages: List[str] = Field(default=[], sa_column=Column(JSON))
    boatLicense: Optional[str] = None
    insuranceNumber: Optional[str] = None
    status: Optional[UserStatus] = None
    activityType: Optional[ActivityType] = None
    company: Optional[str] = None
    siret: Optional[str] = None
    rc: Optional[str] = None

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    birthDate: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    postalCode: Optional[str] = None
    city: Optional[str] = None
    avatarUrl: Optional[str] = None
    languages: Optional[List[str]] = None
    boatLicense: Optional[str] = None
    insuranceNumber: Optional[str] = None
    status: Optional[UserStatus] = None
    activityType: Optional[ActivityType] = None
    company: Optional[str] = None
    siret: Optional[str] = None
    rc: Optional[str] = None
