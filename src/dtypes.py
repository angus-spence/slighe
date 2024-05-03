import time
import csv
from enum import Enum
from dataclasses import dataclass, field

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

class CorridorLoadMethod(Enum):
    from_csv = 1

@dataclass
class Stop:
    stop_id: str
    stop_name: str
    stop_latitude: float
    stop_longitude: float
    settlement: str
    county: str

    def __str__(self) -> str:
        return f'{self.stop_id}: {self.stop_name.upper()} IN {self.settlement.upper()}'
    
@dataclass
class StopTime: 
    stop_id: str
    arrival_time: float
    departure_time: float

    def __str__(self) -> str:
        return f'ARRIVAL TIME: {time.strftime("%H:%M:%S", self.arrival_time)}\nDEPARTURE TIME: {time.strftime("%H:%M:%S", self.departure_time)}'

@dataclass
class Trip:
    trip_id: str
    route_id: str
    stops: list[Stop]
    stop_times: list[StopTime]
    stop_sequence: dict[Stop: int]

@dataclass
class Route:
    route_id: str
    agency_id: str
    route_short_name: str
    route_long_name: str
    route_type: int
    trips: list[Trip]

@dataclass
class Corridor:
    corridor_id: int
    corridor_name: str
    stops: list[Stop] = field(default_factory=list)
    routes: list[Route] = field(default_factory=list)

    def __contains__(self, service) -> bool:
        return service in self.routes

    def _get_frequency(self, start_time: str, end_time: str, day_of_week: DayOfWeek) -> list:
        return

    def _build_timetable(self) -> ...:
        return

    def to_csv(self, path: str) -> None:
        pass