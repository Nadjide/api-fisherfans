from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import users, boats, trips, reservations, logbooks

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(boats.router)
app.include_router(trips.router)
app.include_router(reservations.router)
app.include_router(logbooks.router)


@app.get("/")
def read_root():
    return {"Hello": "FisherFans"}
