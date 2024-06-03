from dtypes import Stop, StopTime, Trip, Route, Corridor, TripTimetable
import dload
import _context

from itertools import chain

class StopBaseConstructor:
    def __init__(self, stop_ids: list[Stop], gtfs_loader: dload.BaseDataLoader) -> None: self.stop_ids, self.gtfs_loader = stop_ids, gtfs_loader
    def __call__(self) -> list[Stop]: return self.build()
    def build(self) -> list[Stop]: return [Stop(row['stop_id'], row['stop_name'], row['stop_lat'], row['stop_lon'], row['settlement'], row['county']) for row in self.gtfs_loader.load(dload.LoadCSVFiles.STOPS) if row['stop_id'] in self.stop_ids]

class StopTimeBaseConstructor:
    def __init__(self, trip_ids: Trip, gtfs_loader: dload.BaseDataLoader) -> None: self.trip_ids, self.gtfs_loader = trip_ids, gtfs_loader
    def __call__(self) -> list[StopTime]: return self.build()
    def build(self) -> list[StopTime]: return [StopTime(row['trip_id'], row['stop_id'], row['stop_sequence'], row['arrival_time'], row['departure_time']) for row in self.gtfs_loader.load(dload.LoadCSVFiles.STOP_TIMES) if row['trip_id'] in self.trip_ids]

class TripBaseConstructor:
    def __init__(self, route_ids: list[Route], gtfs_loader: dload.BaseDataLoader) -> None: self.route_ids, self.gtfs_loader = route_ids, gtfs_loader; self.__post_init__()
    def __post_init__(self) -> None: self._trip_ids = self._call_trip_ids(); self._stop_ids = self._call_stop_ids()
    def __call__(self) -> list[Trip]: return self.build()
    def _call_trip_ids(self) -> list: return [row['trip_id'] for row in self.gtfs_loader.load(dload.LoadCSVFiles.TRIPS) if row['route_id'] in self.route_ids] 
    def _call_stop_ids(self) -> list: return [row['stop_id'] for row in self.gtfs_loader.load(dload.LoadCSVFiles.STOP_TIMES) if row['trip_id'] in self._trip_ids]
    @_context.timing(f'TripBaseConstructor.build')
    def build(self) -> list[Trip]: return [Trip(row['trip_id'], row['route_id'], row['direction_id'], int(row['service_id']), StopBaseConstructor(self._stop_ids, self.gtfs_loader).build(), StopTimeBaseConstructor(self._trip_ids, self.gtfs_loader).build(), None) for row in self.gtfs_loader.load(dload.LoadCSVFiles.TRIPS) if row['route_id'] in self.route_ids]

class StopSequenceConstructor:
    def __int__(self, trip_id: Trip, gtfs_loader: dload.BaseDataLoader) -> None: self.trip_id, self.gtfs_loader = trip_id, gtfs_loader
    def __call__(self) -> dict[Stop: int]: return self.build()
    def build(self) -> dict[Stop: int]: return {row['stop_id']: row['stop_sequence'] for row in self.gtfs_loader.load(dload.LoadCSVFiles.TRIPS) if row['trip_id'] in self.trip_id}

class RouteConstructor:
    def __init__(self, route_ids: list[Route], gtfs_loader: dload.BaseDataLoader) -> None: self.route_ids, self.gtfs_loader = route_ids, gtfs_loader
    def __call__(self) -> list[Route]: self.build()
    def build(self) -> list[Route]: return [Route(row['route_id'], row['agency_id'], row['route_short_name'], row['route_long_name'], row['route_type'], TripBaseConstructor(self.route_ids, self.gtfs_loader).build()) for row in self.gtfs_loader.load(dload.LoadCSVFiles.ROUTES) if row['route_id'] in self.route_ids]

class CorridorConstructor:
    def __init__(self, corridor_id: int, corridor_name: str, route_ids: list[Route], gtfs_loader: dload.BaseDataLoader) -> None: self.corridor_id, self.corridor_name, self.route_ids, self.gtfs_loader = corridor_id, corridor_name, route_ids, gtfs_loader
    def __call__(self) -> Corridor: return self.build() 
    def build(self) -> Corridor: return Corridor(self.corridor_id, self.corridor_name, RouteConstructor(self.route_ids, self.gtfs_loader).build())

class TripTimetableConstructor:
    def __init__(self, corridor: Corridor, gtfs_loader: dload.BaseDataLoader) -> None: self.corridor, self.gtfs_loader = corridor, gtfs_loader
    def __call__(self) -> TripTimetable: return self.build()
    def build(self) -> dict[Trip, TripTimetable]:
        stops, stop_times = self.corridor.pull_stops(), self.corridor.pull_stop_times()
        trips = TripBaseConstructor(self.corridor.routes, self.gtfs_loader).build()
        self._base_headers = [i for i in stops[0].__dict__.keys()]
        trip_timetables = {}
        for trip in trips:
            stop_seq = StopSequenceConstructor(trip, self.gtfs_loader)
            _full_headers = [self._base_headers] + ['stop_sequence'] + [trip.trip_id]
            data = [dict(zip(_full_headers, [0 for _ in range(len(stops))])) for _ in stops]
            _idx = 0
            for row in data:
                r_stop_times = {stop.trip_id: stop.arrival_time for stop in stop_times if stop.stop_id == stops[_idx].stop_id and stop.trip_id == trip}
                stop_seq = StopSequenceConstructor(trip)
                row.update({'stop_id': stops[_idx].stop_id, 
                            'stop_name': stops[_idx].stop_name, 
                            'stop_latitude': stops[_idx].stop_latitude, 
                            'stop_longitude': stops[_idx].stop_longitude,
                            'settlement': stops[_idx].settlement,
                            'county': stops[_idx].county,
                            'stop_seqence': stop_seq[stops[_idx]]})
                row.update(r_stop_times)
                _idx += 1
            trip_timetables[trip] = TripTimetable(stops, trips, data)
        return trip_timetables

#TODO: IMPLEMENT THIS
class CorrdidorTimetableConstructor:
    pass

if __name__ == "__main__":
    loader = dload.GTFSLoadCSV('./data/agency.csv', './data/calendar.csv', './data/calendar_dates.csv', './data/routes.csv', './data/stop_times.csv', './data/stops.csv', './data/trips.csv')
    c = CorridorConstructor(1, 'test', ['2991_37732', '2990_40267', '3038_40330'], loader).build()
    t = TripTimetableConstructor(c, loader).build()
    _exp = c.routes[0].trips[0]
    print(_exp)
    t[_exp].to_csv('timetable.csv')