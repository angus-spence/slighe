from dtypes import Stop, StopTime, Corridor, ServiceTypes

from dataclasses import dataclass
from typing import Optional, Union
from itertools import chain
import csv
import functools

#@functools.lru_cache(maxsize=None)
def pull_stops(corridor: Corridor) -> list[Stop]:
    if not isinstance(corridor, Corridor): raise TypeError(f'corridor: {type(corridor)} is not Corridor')
    return list(chain.from_iterable(list(chain.from_iterable([[[trip.stops[i] for i in range(len(trip.stops))] for trip in route.trips] for route in corridor.routes]))))

@functools.lru_cache(maxsize=None)
def pull_stop_times(corridor: Corridor) -> list[StopTime]:
    if not isinstance(corridor, Corridor): raise TypeError(f'corridor: {type(corridor)} is not Corridor')
    return list(chain.from_iterable(list(chain.from_iterable([[[trip.stop_times[i] for i in range(len(trip.stop_times))] for trip in route.trips] for route in corridor.routes]))))

@dataclass(repr=False)
class Timetable:
    corridor: Corridor
    service_types: list[ServiceTypes]
    settlement_filter: list[str] = None

    def __call__(self, time_start: Optional[Union[str, float]], time_end: Optional[Union[str, float]]) -> None: return self._build_timetable(time_start, time_end) 

    def _build_timetable(self, 
                         time_start: Optional[Union[str, float]], 
                         time_end: Optional[Union[str, float]]) -> None:
        stops, stop_times = pull_stops(self.corridor), pull_stop_times(self.corridor)
        unique_trips = list(set([stoptime.trip_id for stoptime in stop_times]))
        cols = [self._trip_column(stop_times, trip) for trip in unique_trips]
        self._struct = {stop.stop_id: {trip: cols[i][j] for i, trip in enumerate(unique_trips)} for j, stop in enumerate(stops)}
        print(self._struct)

    def _trip_column(self, stops: list[StopTime], trip_id: str) -> list[str]:
        if not isinstance(stops[0], StopTime): raise TypeError(f'stops: {type(stops[0])} is not StopTime')
        return [stop.arrival_time if stop.trip_id == trip_id and stop.arrival_time else 0 for stop in stops]

    def to_csv(self, path: str) -> None:
        with open(path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['stop_id', *(str(trip) for trip in self._struct.keys())]) #TODO: FIX THIS
            writer.writeheader()
            for stop_id, trips in self._struct.items():
                writer.writerow({'stop_id': stop_id, **trips})

if __name__ == "__main__":
    import constructors, dload
    loader = dload.GTFSLoadCSV('./data/agency.csv', './data/calendar.csv', './data/calendar_dates.csv', './data/routes.csv', './data/stop_times.csv', './data/stops.csv', './data/trips.csv')
    c = constructors.CorridorConstructor('1', 'test', ['2991_37732', '2990_40267', '3038_40330'], loader).build()
    t = Timetable(c, [ServiceTypes.MON_FRI])
    t("","")
    t.to_csv('./data/timetable.csv')