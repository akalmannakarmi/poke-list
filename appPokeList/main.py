from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import init_db
from . import models
from . import fetchData

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Fetching Data Please Wait ...")
    # await fetchData.fetch_all_pokemon()
    print("Loaded All Data")
    yield

app = FastAPI(lifespan=lifespan)


from .v1 import endpoints as v1_endpoints
from .v2 import endpoints as v2_endpoints

app.include_router(v1_endpoints.router, prefix="/api/v1")
app.include_router(v2_endpoints.router, prefix="/api/v2")