from transforms import TimeTransforms

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Union, Self, Generator
from itertools import chain
import csv
import re

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
    stop_sequence: int
    arrival_time: Optional[Union[str, float]]
    departure_time: Optional[Union[str, float]]

    def __str__(self) -> str: return f'ARRIVAL TIME: {self.arrival_time}\nDEPARTURE TIME: {self.departure_time}' #TODO: THIS WONT WORK FOR STR AND DATETIME TYPES
    def __lt__(self, other: Self) -> bool: return TimeTransforms.ts_val(self.arrival_time) < TimeTransforms.ts_val(other.arrival_time)
    def __gt__(self, other: Self) -> bool: return TimeTransforms.ts_val(self.arrival_time) > TimeTransforms.ts_val(other.arrival_time)
    def __eq__(self, other: Self) -> bool: return TimeTransforms.ts_val(self.arrival_time) == TimeTransforms.ts_val(other.arrival_time)
    def __le__(self, other: Self) -> bool: return TimeTransforms.ts_val(self.arrival_time) <= TimeTransforms.ts_val(other.arrival_time)
    def __ge__(self, other: Self) -> bool: return TimeTransforms.ts_val(self.arrival_time) >= TimeTransforms.ts_val(other.arrival_time)
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

    def pull_stops(self) -> list[Stop]: return list(chain.from_iterable(list(chain.from_iterable([[[trip.stops[i] for i in range(len(trip.stops))] for trip in route.trips] for route in self.routes]))))
    def pull_stop_times(self) -> list[StopTime]: return list(chain.from_iterable(list(chain.from_iterable([[[trip.stop_times[i] for i in range(len(trip.stop_times))] for trip in route.trips] for route in self.routes]))))
    def pull_trips(self) -> list[Trip]: return list(chain.from_iterable([route.trips for route in self.routes]))

@dataclass(frozen=True)
class TripTimetable:
    stops: list[Stop]
    trip: Trip
    data: list[dict]       

    def filter_by(self, 
                  time: tuple[Optional[Union[str, float]]] = None,
                  service_type: list[ServiceTypes] = None,
                  settlement: list[str] = None,
                  county: list[str] = None
                  ) -> ...:
        """
        Filter the timetable by time, settlement, service type and county

        time: tuple[Optional[Union[str, float]]] = None
            time as a tuple of strings or floats for start and end times
        settlement: list[str] = None
            settlements to filter by
        county: list[str] = None
            counties to filter by
        """
        return NotImplementedError
    
    def sort_by_time(self, ascending: bool = True) -> ...:
        if ascending: self.data.sort(key=lambda x: TimeTransforms.ts_val(x['stop_time']))
        else: self.data.sort(key=lambda x: TimeTransforms.ts_val(x['stop_time']), reverse=True)

    def to_csv(self, file_path: str) -> ...:
        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(self.data[0].keys()))
            writer.writeheader()
            for row_data in self.data:
                writer.writerow(row_data)

@dataclass(frozen=True)
class CorridorTimetable:
    stops: list[Stop]
    trips: list[Trip]
    data: list[dict]

    def filter_by(self, 
                time: tuple[Optional[Union[str, float]]] = None,
                service_type: list[ServiceTypes] = None,
                settlement: list[str] = None,
                county: list[str] = None
                ) -> ...:
        """
        Filter the timetable by time, settlement, service type and county

        time: tuple[Optional[Union[str, float]]] = None
            time as a tuple of strings or floats for start and end times
        settlement: list[str] = None
            settlements to filter by
        county: list[str] = None
            counties to filter by
        """
        return NotImplementedError

    def sort_by_time(self, ascending: bool = True) -> Self:
        tf = re.compile(r'\d{2}:\d{2}:\d{2}')
        row_mins = [min(TimeTransforms.ts_val(v) for v in row.values() if v is str and tf.match(v)) for row in self.data]
        print(row_mins)

    def to_csv(self, file_path: str) -> ...:
        with open(file_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(self.data[0].keys()))
            writer.writeheader()
            for row_data in self.data:
                writer.writerow(row_data)