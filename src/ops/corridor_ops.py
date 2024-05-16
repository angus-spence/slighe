import dtypes

from dataclasses import dataclass
from typing import Optional, Union
from itertools import chain

def pull_stops(corridor: dtypes.Corridor) -> list[dtypes.Stop]:
    if not isinstance(corridor, dtypes.Corridor): raise TypeError(f'corridor: {type(corridor)} is not dtypes.Corridor')
    return list(chain.from_iterable(list(chain.from_iterable([[[trip.stops[i] for i in range(len(trip.stops))] for trip in route.trips] for route in corridor.routes]))))

def pull_stop_times(corridor: dtypes.Corridor) -> list[dtypes.StopTime]:
    if not isinstance(corridor, dtypes.Corridor): raise TypeError(f'corridor: {type(corridor)} is not dtypes.Corridor')
    return list(chain.from_iterable(list(chain.from_iterable([[[trip.stop_times[i] for i in range(len(trip.stop_times))] for trip in route.trips] for route in corridor.routes]))))

@dataclass
class Timetable:
    corridor: dtypes.Corridor
    service_types: list[dtypes.ServiceTypes]
    settlement_filter: list[str] = None

    def __call__(self, time_start: Optional[Union[str, float]], time_end: Optional[Union[str, float]]) -> None: return self._build_timetable(time_start, time_end) 

    def _build_timetable(self, 
                         time_start: Optional[Union[str, float]], 
                         time_end: Optional[Union[str, float]]) -> None:
        stops, stop_times = pull_stops(self.corridor), pull_stop_times(self.corridor)

        return

    def to_csv(self) -> None: return NotImplementedError





if __name__ == "__main__":
    import constructors, dload
    loader = dload.GTFSLoadCSV('./data/agency.csv', './data/calendar.csv', './data/calendar_dates.csv', './data/routes.csv', './data/stop_times.csv', './data/stops.csv', './data/trips.csv')
    c = constructors.CorridorConstructor('1', 'test', ['2991_37732', '2990_40267', '3038_40330'], loader).build()
    t = Timetable(c, [dtypes.ServiceTypes.MON_FRI])
    t("","")