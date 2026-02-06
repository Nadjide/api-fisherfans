from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from app.database import get_session
from app.auth import get_current_user, get_password_hash
from app.models.user import User, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Check for duplicate email
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User.model_validate(user, update={"hashed_password": hashed_password})
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserRead])
def read_users(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    status: Optional[str] = None,
    city: Optional[str] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = select(User).offset(offset).limit(limit)
    if status:
        query = query.where(User.status == status)
    if city:
        query = query.where(User.city == city)
    users = session.exec(query).all()
    return users

@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Optional: basic security check - only allow users to update their own profile?
    # The spec doesn't explicitly mandate this for the "private" API but it's good practice.
    # However, let's stick to the simplest implementation first.
    
    user_data = user_update.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    
    if user_update.password:
        db_user.hashed_password = get_password_hash(user_update.password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # BN6: RGPD Anonymization
    user.firstName = "ANONYMIZED"
    user.lastName = "ANONYMIZED"
    user.email = f"deleted_{user_id}@fisherfans.io"
    user.phone = None
    user.address = None
    user.postalCode = None
    user.city = None
    user.avatarUrl = None
    user.hashed_password = "DELETED"
    user.boatLicense = None
    user.insuranceNumber = None
    user.company = None
    user.siret = None
    user.rc = None
    
    session.add(user)
    session.commit()
