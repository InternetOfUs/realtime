from sqlalchemy.orm import Session

from wenet_realtime.realtime_db import models, schemas
from wenet_realtime.tools import space_distance_m


def create_or_update(db: Session, user_location: schemas.UserLocation):
    db_user_location = models.UserLocation(**user_location.dict())
    db.merge(db_user_location)
    db.commit()


def get_closest(db: Session, location: schemas.Location, max: int = 10):
    users_locations = db.query(models.UserLocation).all()
    return sorted(
        [
            (space_distance_m_from_entity(location, user), user)
            for user in users_locations
        ],
        key=lambda x: x[0],
    )[:max]


def space_distance_m_from_entity(l1: schemas.Location, l2: schemas.Location):
    return space_distance_m(l1.latitude, l1.longitude, l2.latitude, l2.longitude)
