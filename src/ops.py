import dtypes

from typing import Optional, Union
from itertools import chain

class StopOps:
    def uclid_distance(stops: list[dtypes.Stop]) -> float: return NotImplementedError

    def _get_stop_times(stop: dtypes.Stop,
                  service_types: list[dtypes.ServiceTypes],
                  routes: list[dtypes.Route]
                  ) -> list[dtypes.StopTime]:
        print([st.value for st in service_types])
        for route in routes:
            for trip in route.trips:
                print(trip.service_id)
        return list(chain.from_iterable(list(chain.from_iterable([[[trip.stop_times[i] for i in range(len(trip.stop_times)) if trip.stop_times[i].stop_id == stop.stop_id and trip.service_id in [st.value for st in service_types]] for trip in route.trips] for route in routes]))))

    def frequency(stop_times: list[dtypes.StopTime],
                  start: Optional[Union[str, float]],
                  end: Optional[Union[str, float]]
                  ) -> float:
        return

class CorridorOps:
    def __init__(self, corridor: dtypes.Corridor) -> None: self.corridor = corridor
    def stop_frequency(self, start: float, end: float, day_of_week: dtypes.ServiceTypes) -> list[float]: return NotImplementedError
    def build_timetable(self) -> ...: NotImplementedError

if __name__ == "__main__":
    import constructors
    import dload
    loader = dload.GTFSLoadCSV('./data/agency.csv', './data/calendar.csv', './data/calendar_dates.csv', './data/routes.csv', './data/stop_times.csv', './data/stops.csv', './data/trips.csv')
    corridor = constructors.RouteConstructor(['2991_37732', '2990_40267', '3038_40330'], loader).build()
    stop = dtypes.Stop(stop_id='852000011', stop_name='Post Office', stop_latitude='54.19213076', stop_longitude='-7.704834099', settlement='Swanlinbar', county='County_Cavan')
    print(StopOps._get_stop_times(
        stop,
        [dtypes.ServiceTypes.MON],
        [corridor[0]]
    ))