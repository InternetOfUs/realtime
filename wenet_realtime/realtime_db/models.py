from time import time

from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from wenet_realtime.realtime_db.database import Base


class UserLocation(Base):
    __tablename__ = "users_locations"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(Integer, default=int(time()))
    latitude = Column(Float)
    longitude = Column(Float)
    accuracy = Column(Integer, default=0)
