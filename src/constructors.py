import dtypes
import dload

class StopBaseConstructor:
    def __init__(self, stop_ids: list[dtypes.Stop.stop_id], gtfs_loader: dload.BaseDataLoader) -> None: self.stop_ids = stop_ids; self.gtfs_loader = gtfs_loader
    def __call__(self) -> list[dtypes.Stop]: self._load()
    def _load(self) -> list[dtypes.Stop]: return [dtypes.Stop(row['stop_id'], row['stop_name'], row['stop_lat'], row['stop_lon'], row['settlement'], row['country']) for row in self.gtfs_loader.stops if row['stop_id'] in self.stop_ids]

class StopTimeBaseConstructor:
    def __init__(self, trip_id: dtypes.Trip.trip_id, gtfs_loader: dload.BaseDataLoader) -> None: self.trip_id = trip_id; self.gtfs_loader = gtfs_loader
    def __call__(self) -> list[dtypes.StopTime]: self._load()
    def _load(self) -> list[dtypes.StopTime]: return [dtypes.Stop(row['stop_id'], row['arrival_time'], row['departure_time']) for row in self.gtfs_loader.stop_times if row['trip_id'] in self.trip_id]

class TripBaseConstructor:
    def __init__(self, route_ids: list[dtypes.Route.route_id], gtfs_loader: dload.BaseDataLoader) -> None: self.route_ids = route_ids; self.gtfs_loader = gtfs_loader
    def __call__(self) -> list[dtypes.Trip]: self._load_from_csv()
    def _call_stop_ids(self) -> list[dtypes.Stop.stop_id]: return [row['stop_id'] for row in self.gtfs_loader.stops if row['route_id'] in self.route_ids]
    def _call_trip_ids(self) -> list[dtypes.Trip.trip_id]: return [row['trip_id'] for row in self.gtfs_loader.trips if row['route_id'] in self.route_ids]
    def _load(self) -> list[dtypes.Trip]: return [dtypes.Trip(row['trip_id'], row['route_id'], row['direction_id'], StopBaseConstructor(self._call_stop_ids(), self.gtfs_loader), StopTimeBaseConstructor(self._call_trip_ids(), self.gtfs_loader)) for row in self.gtfs_loader.trips if row['route_id'] in self.route_ids]

class StopSequenceConstructor:
    def __int__(self, trip_id: dtypes.Trip.trip_id, gtfs_loader: dload.BaseDataLoader) -> None: self.trip_id = trip_id; 
    def __call__(self) -> dict[dtypes.Stop.stop_id: int]: return self._load_from_csv()

class RouteConstructor:
    def __init__(self, route_ids: list[dtypes.Route.route_id], gtfs_loader: dload.BaseDataLoader) -> None: self.route_ids = route_ids; self.gtfs_loader = gtfs_loader
    def __call__(self) -> list[dtypes.Route]: self._load()
    def _load(self) -> list[dtypes.Route]: return [dtypes.Route(row['route_id'], row['agency_id'], row['route_short_name'], row['route_long_name'], row['route_type'], TripBaseConstructor(self.route_ids, self.gtfs_loader)) for row in self.gtfs_loader.routes if row['route_id'] in self.route_ids]

class CorridorConstructor:
    def __init__(self, corridor_id: int, route_ids: list[dtypes.Route.route_id]) -> None: self.corridor_id = corridor_id; self.route_ids = route_ids
    def __call__(self) -> dtypes.Corridor: return dtypes.Corridor(self.corridor_id, StopBaseConstructor(self.stop_ids))



if __name__ == "__main__":
    loader = dload.GTFSLoadCSV('./data/agency.csv', './data/calendar.csv', './data/calendar_dates.csv', './data/routes.csv', './data/stop_times.csv', './data/stops.csv', './data/trips.csv')
    CorridorConstructor(1, ['2991_37732', '2991_37732'])()