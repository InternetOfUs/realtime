from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from wenet_realtime.realtime_db import crud, models, schemas
from wenet_realtime.realtime_db.database import SessionLocal, engine
import logging
from wenet_realtime import config
from wenet_realtime.wenet_logging import create_ch_handler, create_log_file_handler
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    ch = create_ch_handler()
    log_file = create_log_file_handler()
    logger.addHandler(ch)
    logger.addHandler(log_file)


@app.post("/users_locations/")
def create_user(user: schemas.UserLocation, db: Session = Depends(get_db)):
    crud.create_or_update(db, user)


@app.post("/locations/", response_model=schemas.LocationsOut)
def get_locations(user_list: schemas.UsersList, db: Session = Depends(get_db)):
    user_ids = [user_id for user_id in user_list.userids]
    user_locations = crud.get_locations(db, user_ids)
    res = schemas.LocationsOut(locations=user_locations)
    return res


@app.get("/closest/")
def closest_users(
    latitude: float,
    longitude: float,
    nb_user_max: int = 10,
    db: Session = Depends(get_db),
):
    crud.clean_old_records(db)
    return crud.get_closest(
        db, schemas.Location(latitude=latitude, longitude=longitude), nb_user_max
    )

