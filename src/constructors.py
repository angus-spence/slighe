from dtypes import Stop, StopTime, Trip, Route, Corridor, TripTimetable, CorridorTimetable
import dload
import _context

class StopBaseConstructor:
    def __init__(self, stop_ids: list[Stop], gtfs_loader: dload.BaseDataLoader) -> None: self.stop_ids, self.gtfs_loader = stop_ids, gtfs_loader
    def __call__(self) -> list[Stop]: return self.build()
    def build(self) -> list[Stop]: return [Stop(row['stop_id'], row['stop_name'], row['stop_lat'], row['stop_lon'], row['settlement'], row['county']) for row in self.gtfs_loader.load(dload.LoadCSVFiles.STOPS) if row['stop_id'] in self.stop_ids]

class StopTimeBaseConstructor:
    def __init__(self, trip_id: Trip, gtfs_loader: dload.BaseDataLoader) -> None: self.trip_id, self.gtfs_loader = trip_id, gtfs_loader
    def __call__(self) -> list[StopTime]: return self.build()
    def build(self) -> list[StopTime]: return [StopTime(row['trip_id'], row['stop_id'], row['stop_sequence'], row['arrival_time'], row['departure_time']) for row in self.gtfs_loader.load(dload.LoadCSVFiles.STOP_TIMES) if row['trip_id'] in self.trip_id]

class StopSequenceConstructor:
    def __init__(self, trip_id: Trip, gtfs_loader: dload.BaseDataLoader) -> None: self.trip_id, self.gtfs_loader = trip_id, gtfs_loader
    def __call__(self) -> dict[Stop: int]: return self.build()
    def build(self) -> dict[Stop: int]: return {row['stop_id']: row['stop_sequence'] for row in self.gtfs_loader.load(dload.LoadCSVFiles.STOP_TIMES) if row['trip_id'] == self.trip_id}

class TripBaseConstructor:
    def __init__(self, route_ids: list[Route], gtfs_loader: dload.BaseDataLoader) -> None: self.route_ids, self.gtfs_loader = route_ids, gtfs_loader; self.__post_init__()
    def __post_init__(self) -> None: self._trip_ids = self._call_trip_ids(); self._stop_ids = self._call_stop_ids()
    def __call__(self) -> list[Trip]: return self.build()
    def _call_trip_ids(self) -> list: return [row['trip_id'] for row in self.gtfs_loader.load(dload.LoadCSVFiles.TRIPS) if row['route_id'] in self.route_ids] 
    def _call_stop_ids(self) -> list: return [row['stop_id'] for row in self.gtfs_loader.load(dload.LoadCSVFiles.STOP_TIMES) if row['trip_id'] in self._trip_ids]
    @_context.timing(f'TripBaseConstructor.build')
    def build(self) -> list[Trip]: return [Trip(row['trip_id'], row['route_id'], row['direction_id'], int(row['service_id']), StopBaseConstructor(self._stop_ids, self.gtfs_loader).build(), StopTimeBaseConstructor(row['trip_id'], self.gtfs_loader).build(), StopSequenceConstructor(row['trip_id'], self.gtfs_loader).build()) for row in self.gtfs_loader.load(dload.LoadCSVFiles.TRIPS) if row['route_id'] in self.route_ids]

class RouteConstructor:
    def __init__(self, route_ids: list[Route], gtfs_loader: dload.BaseDataLoader) -> None: self.route_ids, self.gtfs_loader = route_ids, gtfs_loader
    def __call__(self) -> list[Route]: self.build()
    def build(self) -> list[Route]: return [Route(row['route_id'], row['agency_id'], row['route_short_name'], row['route_long_name'], row['route_type'], TripBaseConstructor(self.route_ids, self.gtfs_loader).build()) for row in self.gtfs_loader.load(dload.LoadCSVFiles.ROUTES) if row['route_id'] in self.route_ids]

class CorridorConstructor:
    def __init__(self, corridor_id: int, corridor_name: str, route_ids: list[Route], gtfs_loader: dload.BaseDataLoader) -> None: self.corridor_id, self.corridor_name, self.route_ids, self.gtfs_loader = corridor_id, corridor_name, route_ids, gtfs_loader
    def __call__(self) -> Corridor: return self.build() 
    def build(self) -> Corridor: return Corridor(self.corridor_id, self.corridor_name, RouteConstructor(self.route_ids, self.gtfs_loader).build())

class TripTimetableConstructor:
    def __init__(self, trip: Trip) -> None: self.trip = trip
    def __call__(self) -> TripTimetable: return self.build()
    def build(self) -> TripTimetable:
        timetable = [dict(zip(self.trip.stops[0].__dict__.keys(), [0 for _ in range(len(self.trip.stops[0].__dict__.keys()))])) for _ in self.trip.stop_times]
        _idx = 0
        for stop_time in self.trip.stop_times:
            stop = next(filter(lambda x: x.stop_id == stop_time.stop_id, self.trip.stops))
            timetable[_idx].update({'stop_id': stop.stop_id, 
                                    'stop_name': stop.stop_name, 
                                    'stop_latitude': stop.stop_latitude, 
                                    'stop_longitude': stop.stop_longitude, 
                                    'settlement': stop.settlement,
                                    'county': stop.county,
                                    'stop_sequence': stop_time.stop_sequence,
                                    'stop_time': stop_time.arrival_time})
            _idx += 1  
        return TripTimetable(self.trip.stops, self.trip, timetable)

class CorrdidorTimetableConstructor:
    def __init__(self, corridor: Corridor) -> None: self.corridor = corridor
    def __call__(self) -> None: return self.build()
    def build(self) -> CorridorTimetable:
        trip_timetables = [TripTimetableConstructor(trip).build() for route in self.corridor.routes for trip in route.trips]
        unique_stops = list(set(self.corridor.pull_stops()))
        timetable = []
        for stop in unique_stops:
            timetable.append({trip_timetable.trip.trip_id: trip_timetable.data[i]['stop_time'] if trip_timetable.data[i]['stop_id'] == stop.stop_id else None for trip_timetable in trip_timetables for i in range(len(trip_timetable.data))})
        return CorridorTimetable(unique_stops, self.corridor.pull_trips(), timetable)

if __name__ == "__main__":
    loader = dload.GTFSLoadCSV('./data/agency.csv', './data/calendar.csv', './data/calendar_dates.csv', './data/routes.csv', './data/stop_times.csv', './data/stops.csv', './data/trips.csv')
    c = CorridorConstructor(1, 'test', ['2991_37732', '2990_40267', '3038_40330'], loader).build()
    ct = CorrdidorTimetableConstructor(c).build()
    ct = ct.sort_by_time()
    ct.to_csv('corridor_timetable.csv')