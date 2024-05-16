from enum import Enum

import datetime

BASE_DAY = datetime.datetime.min

class CRS(Enum):
    OSGB36 = 1

class GeoTransforms:
    def __init__(self):
        pass

    def d2m(self, lat1: float, lon1: float) -> float:
        """
        degrees to meters
        """
        
def ts_to_float(time: str, form: str) -> float:
    return datetime.datetime.strptime(time, form).replace(tzinfo=datetime.timezone.utc).timestamp()