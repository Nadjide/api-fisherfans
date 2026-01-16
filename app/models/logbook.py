from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
import datetime

class LogbookBase(SQLModel):
    title: str
    authorId: int = Field(foreign_key="user.id")
    createdAt: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class Logbook(LogbookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class LogbookCreate(LogbookBase):
    pass

class LogbookRead(LogbookBase):
    id: int

class LogbookPageBase(SQLModel):
    fishName: str
    photoUrl: Optional[str] = None
    comment: Optional[str] = None
    lengthCm: Optional[int] = None
    weightKg: Optional[float] = None
    fishingLocation: Optional[str] = None
    fishingDate: datetime.date
    released: Optional[bool] = False
    logbookId: int = Field(foreign_key="logbook.id")

class LogbookPage(LogbookPageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class LogbookPageCreate(LogbookPageBase):
    pass

class LogbookPageRead(LogbookPageBase):
    id: int

class LogbookPageUpdate(SQLModel):
    fishName: Optional[str] = None
    photoUrl: Optional[str] = None
    comment: Optional[str] = None
    lengthCm: Optional[int] = None
    weightKg: Optional[float] = None
    fishingLocation: Optional[str] = None
    fishingDate: Optional[datetime.date] = None
    released: Optional[bool] = None
    logbookId: Optional[int] = None
