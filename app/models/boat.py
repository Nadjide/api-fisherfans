from typing import List, Optional
from enum import Enum
from sqlmodel import SQLModel, Field, JSON, Column

class RequiredLicense(str, Enum):
    coastal = "coastal"
    inland = "inland"

class BoatType(str, Enum):
    open = "open"
    cabin = "cabin"
    catamaran = "catamaran"
    sailboat = "sailboat"
    jetski = "jetski"
    canoe = "canoe"

class Propulsion(str, Enum):
    diesel = "diesel"
    gasoline = "gasoline"
    none = "none"

class BoatBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None
    brand: Optional[str] = None
    yearBuilt: Optional[int] = None
    photoUrl: Optional[str] = None
    requiredLicense: Optional[RequiredLicense] = None
    boatType: BoatType
    equipment: List[str] = Field(default=[], sa_column=Column(JSON))
    depositEUR: Optional[float] = None
    maxCapacity: Optional[int] = None
    berths: Optional[int] = None
    homePort: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    propulsion: Optional[Propulsion] = None
    enginePowerHP: Optional[int] = None
    ownerId: int = Field(foreign_key="user.id")

class Boat(BoatBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class BoatCreate(BoatBase):
    pass

class BoatRead(BoatBase):
    id: int

class BoatUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    yearBuilt: Optional[int] = None
    photoUrl: Optional[str] = None
    requiredLicense: Optional[RequiredLicense] = None
    boatType: Optional[BoatType] = None
    equipment: Optional[List[str]] = None
    depositEUR: Optional[float] = None
    maxCapacity: Optional[int] = None
    berths: Optional[int] = None
    homePort: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    propulsion: Optional[Propulsion] = None
    enginePowerHP: Optional[int] = None
    ownerId: Optional[int] = None
