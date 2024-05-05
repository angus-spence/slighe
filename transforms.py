from enum import Enum

class CRS(Enum):
    OSGB36 = 1

class GeoTransforms:
    def __init__(self):
        pass

    def d2m(self, lat1: float, lon1: float) -> float:
        """
        degrees to meters
        """
        
        