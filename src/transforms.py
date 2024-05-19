from enum import Enum
from typing import Optional, Union

import datetime

BASE_DAY = datetime.datetime.min

class CRS(Enum):
    OSGB36 = 1

class GeoTransforms:
    @staticmethod
    def d2m(self, lat1: float, lon1: float) -> float:
        """
        degrees to meters
        """

class TimeTransforms:
    @staticmethod
    def ts_val(time: Optional[Union[str, float]]) -> float:
        if isinstance(time, float): return time
        elif isinstance(time, str): return TimeTransforms.ts_to_float(time, "%H:%M:%S")
    @staticmethod
    def ts_to_float(time: str, form: str) -> float:
        return datetime.datetime.strptime(time, form).replace(tzinfo=datetime.timezone.utc).timestamp()