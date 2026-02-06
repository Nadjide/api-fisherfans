from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from app.database import get_session
from app.auth import get_current_user
from app.models.user import User
from app.models.boat import Boat, BoatCreate, BoatRead, BoatUpdate
from app.models.user import User

router = APIRouter(prefix="/boats", tags=["Boats"])

@router.post("/", response_model=BoatRead, status_code=status.HTTP_201_CREATED)
def create_boat(
    boat: BoatCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    owner = session.get(User, boat.ownerId)
    if not owner:
        raise HTTPException(status_code=404, detail="User not found")
    if not owner.boatLicense:
        raise HTTPException(status_code=400, detail="Boat license required")

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
    brand: Optional[str] = None,
    boatType: Optional[str] = None,
    homePort: Optional[str] = None,
    minLat: Optional[float] = None,
    maxLat: Optional[float] = None,
    minLng: Optional[float] = None,
    maxLng: Optional[float] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = select(Boat).offset(offset).limit(limit)
    if userId:
        query = query.where(Boat.ownerId == userId)
    if brand:
        query = query.where(Boat.brand == brand)
    if boatType:
        query = query.where(Boat.boatType == boatType)
    if homePort:
        query = query.where(Boat.homePort == homePort)

    bbox_params = [minLat, maxLat, minLng, maxLng]
    if any(param is not None for param in bbox_params):
        if not all(param is not None for param in bbox_params):
            raise HTTPException(
                status_code=400,
                detail="Bounding box requires minLat, maxLat, minLng, maxLng"
            )
        query = query.where(
            Boat.latitude >= minLat,
            Boat.latitude <= maxLat,
            Boat.longitude >= minLng,
            Boat.longitude <= maxLng,
        )
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
