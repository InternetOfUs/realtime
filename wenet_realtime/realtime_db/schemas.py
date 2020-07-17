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
