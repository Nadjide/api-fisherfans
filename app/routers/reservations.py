from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from app.database import get_session
from app.auth import get_current_user
from app.models.reservation import Reservation, ReservationCreate, ReservationRead, ReservationUpdate
from app.models.user import User
from app.models.trip import Trip

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("/", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation: ReservationCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Validate user exists
    user = session.get(User, reservation.userId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate trip exists
    trip = session.get(Trip, reservation.tripId)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    db_reservation = Reservation.model_validate(reservation)
    session.add(db_reservation)
    session.commit()
    session.refresh(db_reservation)
    return db_reservation

@router.get("/", response_model=List[ReservationRead])
def read_reservations(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    userId: Optional[int] = None,
    tripId: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = select(Reservation).offset(offset).limit(limit)
    if userId:
        query = query.where(Reservation.userId == userId)
    if tripId:
        query = query.where(Reservation.tripId == tripId)
    reservations = session.exec(query).all()
    return reservations

@router.get("/{reservation_id}", response_model=ReservationRead)
def read_reservation(
    reservation_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.put("/{reservation_id}", response_model=ReservationRead)
def update_reservation(
    reservation_id: int, 
    reservation_update: ReservationUpdate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_reservation = session.get(Reservation, reservation_id)
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    reservation_data = reservation_update.model_dump(exclude_unset=True)
    db_reservation.sqlmodel_update(reservation_data)
    
    session.add(db_reservation)
    session.commit()
    session.refresh(db_reservation)
    return db_reservation

@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(
    reservation_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    session.delete(reservation)
    session.commit()
