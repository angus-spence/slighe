from transforms import TimeTransforms

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Union

class DayOfWeek(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6

class ServiceTypes(Enum):
    NO_SERVICE = 0
    MON_FRI = 1
    MON = 2
    TUE = 3
    WED = 4
    THU = 5
    FRI = 6
    SAT = 7
    SUN = 8 
    MON_THU = 9
    MON_SAT = 10
    MON_SUN = 11
    MON_THU_SAT = 13
    TUE_THU = 14
    MON_PLUS_SUN = 15
    SAT_SUN = 16
    MON_PLUS_FRI = 17
    MON_PLUS_FRI_PLUS_SAT = 18
    FRI_SAT = 19
    FRI_SUN = 20
    TUE_PLUS_THU = 21
    MON_FRI_PLUS_SUN = 25
    FRI_PLUS_SUN = 27
    TUE_FRI = 28

@dataclass(frozen=True)
class Stop:
    stop_id: str
    stop_name: str
    stop_latitude: float
    stop_longitude: float
    settlement: str
    county: str

    def __str__(self) -> str: return f'{self.stop_id}: {self.stop_name.upper()} IN {self.settlement.upper()}'
    
@dataclass(frozen=True)
class StopTime: 
    trip_id: str
    stop_id: str
    arrival_time: Optional[Union[str, float]]
    departure_time: Optional[Union[str, float]]

    def __str__(self) -> str: return f'ARRIVAL TIME: {self.arrival_time}\nDEPARTURE TIME: {self.departure_time}' #TODO: THIS WONT WORK FOR STR AND DATETIME TYPES
    def __lt__(self, other) -> bool: return TimeTransforms.ts_val(self.arrival_time) < TimeTransforms.ts_val(other.arrival_time)
    def __gt__(self, other) -> bool: return TimeTransforms.ts_val(self.arrival_time) > TimeTransforms.ts_val(other.arrival_time)
    def __eq__(self, other) -> bool: return TimeTransforms.ts_val(self.arrival_time) == TimeTransforms.ts_val(other.arrival_time)
    def __le__(self, other) -> bool: return TimeTransforms.ts_val(self.arrival_time) <= TimeTransforms.ts_val(other.arrival_time)
    def __ge__(self, other) -> bool: return TimeTransforms.ts_val(self.arrival_time) >= TimeTransforms.ts_val(other.arrival_time)
    def timestring_to_float(self) -> None: self.arrival_time, self.departure_time = TimeTransforms.ts_to_float(self.arrival_time, "%H:%M:%S"), TimeTransforms.ts_to_float(self.departure_time, "%H:%M:%S")
        
@dataclass(frozen=True)
class Trip:
    trip_id: str
    route_id: str
    direction_id: int
    service_id: int
    stops: list[Stop]
    stop_times: list[StopTime]
    stop_sequence: dict[Stop: int]

@dataclass(frozen=True)
class Route:
    route_id: str
    agency_id: str
    route_short_name: str
    route_long_name: str
    route_type: int
    trips: list[Trip]

@dataclass(frozen=True)
class Corridor:
    corridor_id: int
    corridor_name: str
    routes: list[Route]

@dataclass(frozen=True)
class Timetable:
    stops: list[Stop]
    trips: list[Trip]