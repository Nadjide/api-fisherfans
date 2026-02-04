from typing import List, Optional
from enum import Enum
from sqlmodel import SQLModel, Field, JSON, Column
from pydantic import validator
import datetime

class TripType(str, Enum):
    daily = "daily"
    recurring = "recurring"

class PricingType(str, Enum):
    flat = "flat"
    per_person = "per_person"

class TripBase(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tripType: TripType
    pricingType: PricingType
    startDates: List[str] = Field(default=[], sa_column=Column(JSON))
    endDates: List[str] = Field(default=[], sa_column=Column(JSON))
    startTimes: List[str] = Field(default=[], sa_column=Column(JSON))
    # YAML says items: string, format: time. 
    # Let's use List[str] for simplicity in SQLite + JSON, but better to use List[datetime.time] and let Pydantic handle it if possible. 
    # Only standard JSON types are supported in SQLite JSON column usually.
    # We will use simple strings for lists to ensure compatibility with SQLite JSON storage of simple arrays.
    # Actually, let's stick to what we did for User/Boat (JSON).
    
    # Re-defining to List[str] to match the YAML format: date/time generic strings if simpler, 
    # but Pydantic datetime.date is better for validation. 
    # However, SQLModel with JSON column requires some care. 
    # Let's treat them as lists of strings for storage simplicity in SQLite without custom serializers for now, 
    # or rely on Pydantic's JSON serialization.
    # For Lists in SQLModel with SQLite, it's often easiest to store as List[Any] or List[str] with JSON column.
    
    # Let's go with List[str] to correspond to "format: date" (ISO strings) in YAML.
    
    endTimes: List[str] = Field(default=[], sa_column=Column(JSON))
    passengerCount: Optional[int] = None
    price: Optional[float] = None
    boatId: int = Field(foreign_key="boat.id")

    # We need to manually validate that everything is serialized correctly for SQLite JSON
    class Config:
        arbitrary_types_allowed = True

class Trip(TripBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class TripCreate(TripBase):
    pass

class TripRead(TripBase):
    id: int

class TripUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tripType: Optional[TripType] = None
    pricingType: Optional[PricingType] = None
    startDates: Optional[List[str]] = None
    endDates: Optional[List[str]] = None
    startTimes: Optional[List[str]] = None
    endTimes: Optional[List[str]] = None
    passengerCount: Optional[int] = None
    price: Optional[float] = None
    boatId: Optional[int] = None
