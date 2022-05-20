import logging
from typing import List, Optional

import sentry_sdk
from sentry_sdk.integrations.logging import EventHandler

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from wenet_realtime import config
from wenet_realtime.realtime_db import crud, models, schemas
from wenet_realtime.realtime_db.database import SessionLocal, engine
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
    if config.DEFAULT_WENET_SENTRY_KEY != "" and config.DEFAULT_ENV != "dev":
        sentry_sdk.init(config.DEFAULT_WENET_SENTRY_KEY)
        sentry_handler = EventHandler()
        formatter = logging.Formatter(config.DEFAULT_LOGGER_FORMAT)
        sentry_handler.formatter = formatter
        logger.addHandler(sentry_handler)


@app.post("/users_locations/", tags=["Real-time operations"])
def create_user(user: schemas.UserLocation, db: Session = Depends(get_db)):
    crud.create_or_update(db, user)


@app.post(
    "/locations/", tags=["Real-time operations"], response_model=schemas.LocationsOut
)
def get_locations(user_list: schemas.UsersList, db: Session = Depends(get_db)):
    user_ids = [user_id for user_id in user_list.userids]
    user_locations = crud.get_locations(db, user_ids)
    res = schemas.LocationsOut(locations=user_locations)
    return res


@app.get(
    "/closest/",
    tags=["Real-time operations"],
    response_model=List[schemas.ClosestRecord],
)
def closest_users(
    latitude: float,
    longitude: float,
    nb_user_max: int = 10,
    radius: Optional[int] = None,
    db: Session = Depends(get_db),
):
    if not config.DEFAULT_KEEP_OLD_RECORDS:
        crud.clean_old_records(db)
    crud_res = crud.get_closest(
        db, schemas.Location(latitude=latitude, longitude=longitude), nb_user_max
    )
    res = list()
    for k, v in crud_res.items():
        if radius is None or v < radius:
            res.append(schemas.ClosestRecord(userId=k, distance=v))
    return res
