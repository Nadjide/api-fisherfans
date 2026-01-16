from typing import Optional
from sqlmodel import SQLModel, Field
import datetime

class ReservationBase(SQLModel):
    reservedDate: datetime.date
    seats: int
    totalPrice: Optional[float] = None
    userId: int = Field(foreign_key="user.id")
    tripId: int = Field(foreign_key="trip.id")

class Reservation(ReservationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ReservationCreate(ReservationBase):
    pass

class ReservationRead(ReservationBase):
    id: int
