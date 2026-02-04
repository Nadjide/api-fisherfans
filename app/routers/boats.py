from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from app.database import get_session
from app.auth import get_current_user
from app.models.user import User
from app.models.boat import Boat, BoatCreate, BoatRead, BoatUpdate

router = APIRouter(prefix="/boats", tags=["Boats"])

@router.post("/", response_model=BoatRead, status_code=status.HTTP_201_CREATED)
def create_boat(
    boat: BoatCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_boat = Boat.model_validate(boat)
    session.add(db_boat)
    session.commit()
    session.refresh(db_boat)
    return db_boat

@router.get("/", response_model=List[BoatRead])
def read_boats(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    userId: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = select(Boat).offset(offset).limit(limit)
    if userId:
        query = query.where(Boat.ownerId == userId)
    boats = session.exec(query).all()
    return boats

@router.get("/{boat_id}", response_model=BoatRead)
def read_boat(
    boat_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    boat = session.get(Boat, boat_id)
    if not boat:
        raise HTTPException(status_code=404, detail="Boat not found")
    return boat

@router.put("/{boat_id}", response_model=BoatRead)
def update_boat(
    boat_id: int, 
    boat_update: BoatUpdate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_boat = session.get(Boat, boat_id)
    if not db_boat:
        raise HTTPException(status_code=404, detail="Boat not found")
    
    boat_data = boat_update.model_dump(exclude_unset=True)
    db_boat.sqlmodel_update(boat_data)
    
    session.add(db_boat)
    session.commit()
    session.refresh(db_boat)
    return db_boat

@router.delete("/{boat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_boat(
    boat_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    boat = session.get(Boat, boat_id)
    if not boat:
        raise HTTPException(status_code=404, detail="Boat not found")
    session.delete(boat)
    session.commit()
