from typing import List, Optional
from time import time

from pydantic import BaseModel


class UserLocation(BaseModel):
    id: str
    timestamp: Optional[int] = int(time())
    latitude: float
    longitude: float
    accuracy: Optional[int] = 0

    class Config:
        orm_mode = True


class Location(BaseModel):
    latitude: float
    longitude: float

class UsersList(BaseModel):
    userids: List[str]

class ClosestRecord(BaseModel):
    userId: str
    distance: float

class UserLocationOut(BaseModel):
    userId: str
    longitude: Optional[float] = None
    latitude: Optional[float] = None

class LocationsOut(BaseModel):
    locations: Optional[List[UserLocationOut]] = None