from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import auth, users, boats, trips, reservations, logbooks

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router, prefix="/v1")
app.include_router(users.router, prefix="/v1")
app.include_router(boats.router, prefix="/v1")
app.include_router(trips.router, prefix="/v1")
app.include_router(reservations.router, prefix="/v1")
app.include_router(logbooks.router, prefix="/v1")


@app.get("/")
def read_root():
    return {"Hello": "FisherFans"}
