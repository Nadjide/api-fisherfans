from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from app.database import get_session
from app.auth import get_current_user
from app.models.user import User
from app.models.logbook import (
    Logbook, LogbookCreate, LogbookRead,
    LogbookPage, LogbookPageCreate, LogbookPageRead, LogbookPageUpdate
)

router = APIRouter(prefix="/logbooks", tags=["Logbooks"])

# --- Logbooks ---

@router.post("/", response_model=LogbookRead, status_code=status.HTTP_201_CREATED)
def create_logbook(
    logbook: LogbookCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    user = session.get(User, logbook.authorId)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_logbook = Logbook.model_validate(logbook)
    session.add(db_logbook)
    session.commit()
    session.refresh(db_logbook)
    return db_logbook

@router.get("/", response_model=List[LogbookRead])
def read_logbooks(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    userId: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    query = select(Logbook).offset(offset).limit(limit)
    if userId:
        query = query.where(Logbook.authorId == userId)
    logbooks = session.exec(query).all()
    return logbooks

@router.get("/{logbook_id}", response_model=LogbookRead)
def read_logbook(
    logbook_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    logbook = session.get(Logbook, logbook_id)
    if not logbook:
        raise HTTPException(status_code=404, detail="Logbook not found")
    return logbook

@router.delete("/{logbook_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_logbook(
    logbook_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    logbook = session.get(Logbook, logbook_id)
    if not logbook:
        raise HTTPException(status_code=404, detail="Logbook not found")
    session.delete(logbook)
    session.commit()

# --- Logbook Pages ---

@router.get("/{logbook_id}/pages", response_model=List[LogbookPageRead])
def read_logbook_pages(
    logbook_id: int,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    logbook = session.get(Logbook, logbook_id)
    if not logbook:
        raise HTTPException(status_code=404, detail="Logbook not found")
        
    query = select(LogbookPage).where(LogbookPage.logbookId == logbook_id).offset(offset).limit(limit)
    pages = session.exec(query).all()
    return pages

@router.post("/{logbook_id}/pages", response_model=LogbookPageRead, status_code=status.HTTP_201_CREATED)
def create_logbook_page(
    logbook_id: int, 
    page: LogbookPageCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Ensure logbook exists and matches path
    logbook = session.get(Logbook, logbook_id)
    if not logbook:
        raise HTTPException(status_code=404, detail="Logbook not found")
    
    if page.logbookId != logbook_id:
         raise HTTPException(status_code=400, detail="Logbook ID in body does not match path")

    db_page = LogbookPage.model_validate(page)
    session.add(db_page)
    session.commit()
    session.refresh(db_page)
    return db_page

@router.get("/{logbook_id}/pages/{page_id}", response_model=LogbookPageRead)
def read_logbook_page(
    logbook_id: int,
    page_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    page = session.get(LogbookPage, page_id)
    if not page or page.logbookId != logbook_id:
        raise HTTPException(status_code=404, detail="Logbook page not found")
    return page

@router.put("/{logbook_id}/pages/{page_id}", response_model=LogbookPageRead)
def update_logbook_page(
    logbook_id: int,
    page_id: int,
    page_update: LogbookPageUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_page = session.get(LogbookPage, page_id)
    if not db_page or db_page.logbookId != logbook_id:
        raise HTTPException(status_code=404, detail="Logbook page not found")
    
    page_data = page_update.model_dump(exclude_unset=True)
    db_page.sqlmodel_update(page_data)
    
    session.add(db_page)
    session.commit()
    session.refresh(db_page)
    return db_page

@router.delete("/{logbook_id}/pages/{page_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_logbook_page(
    logbook_id: int,
    page_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_page = session.get(LogbookPage, page_id)
    if not db_page or db_page.logbookId != logbook_id:
        raise HTTPException(status_code=404, detail="Logbook page not found")
    
    session.delete(db_page)
    session.commit()

@router.get("/users/{user_id}/pages", response_model=List[LogbookPageRead])
def read_user_logbook_pages(
    user_id: int,
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # This requires joining Logbook and LogbookPage, or fetching logbooks then pages.
    # SQLModel/SQLAlchemy join:
    # SELECT page.* FROM logbookpage page JOIN logbook lb ON page.logbookId = lb.id WHERE lb.authorId = user_id
    
    query = (
        select(LogbookPage)
        .join(Logbook)
        .where(Logbook.authorId == user_id)
        .offset(offset)
        .limit(limit)
    )
    pages = session.exec(query).all()
    return pages
