from time import time
from sqlalchemy.orm import Session

from wenet_realtime.realtime_db import models, schemas
from wenet_realtime.tools import space_distance_m


def create_or_update(db: Session, user_location: schemas.UserLocation):
    db_user_location = models.UserLocation(**user_location.dict())
    db.merge(db_user_location)
    db.commit()


def get_closest(db: Session, location: schemas.Location, nb_user_max: int = 10 * 60):
    users_locations = db.query(models.UserLocation).all()
    return dict(
        sorted(
            [
                (user.id, space_distance_m_from_entity(location, user))
                for user in users_locations
            ],
            key=lambda x: x[1],
        )[:nb_user_max]
    )


def clean_old_records(db: Session, older_than_n_minutes: int = 20):
    current_ts = int(time())
    old_records = db.query(models.UserLocation).filter(
        current_ts - models.UserLocation.timestamp >= older_than_n_minutes
    )
    for old_record in old_records:
        db.delete(old_record)
    db.commit()


def delete_all(db: Session):
    db.query(models.UserLocation).delete()
    db.commit()


def space_distance_m_from_entity(l1: schemas.Location, l2: schemas.Location):
    return space_distance_m(l1.latitude, l1.longitude, l2.latitude, l2.longitude)
