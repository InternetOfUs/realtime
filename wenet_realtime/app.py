from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from wenet_realtime.realtime_db import crud, models, schemas
from wenet_realtime.realtime_db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users_locations/")
def create_user(user: schemas.UserLocation, db: Session = Depends(get_db)):
    crud.create_or_update(db, user)


@app.post("/locations/")
def get_locations(user_list: schemas.UsersList, db: Session = Depends(get_db)):
    user_ids = [user_id for user_id in user_list.userids]
    user_locations = crud.get_locations(db, user_ids)
    return user_locations


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

