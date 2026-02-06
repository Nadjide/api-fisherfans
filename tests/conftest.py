import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

from app.database import get_session
from app.auth import get_current_user
from app.models.user import User
from main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_session_override():
        with Session(engine) as session:
            yield session

    def get_current_user_override():
        return User(
            id=1,
            email="admin@example.com",
            firstName="Admin",
            lastName="User",
            hashed_password="hashedpassword"
        )

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override
    
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
