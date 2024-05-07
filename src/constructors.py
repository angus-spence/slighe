import dtypes
import dload

class StopBaseConstructor:
    def __init__(self, stop_ids: list[dtypes.Stop], gtfs_loader: dload.BaseDataLoader) -> None: self.stop_ids, self.gtfs_loader = stop_ids, gtfs_loader
    def __call__(self) -> list[dtypes.Stop]: return self.build()
    def build(self) -> list[dtypes.Stop]: return [dtypes.Stop(row['stop_id'], row['stop_name'], row['stop_lat'], row['stop_lon'], row['settlement'], row['country']) for row in self.gtfs_loader.load(dload.LoadCSVFiles.STOPS) if row['stop_id'] in self.stop_ids]

class StopTimeBaseConstructor:
    def __init__(self, trip_id: dtypes.Trip, gtfs_loader: dload.BaseDataLoader) -> None: self.trip_id, self.gtfs_loader = trip_id, gtfs_loader
    def __call__(self) -> list[dtypes.StopTime]: return self.build()
    def build(self) -> list[dtypes.StopTime]: return [dtypes.Stop(row['stop_id'], row['arrival_time'], row['departure_time']) for row in self.gtfs_loader.load(dload.LoadCSVFiles.STOP_TIMES) if row['trip_id'] in self.trip_id]

class TripBaseConstructor:
    def __init__(self, route_ids: list[dtypes.Route], gtfs_loader: dload.BaseDataLoader) -> None: self.route_ids, self.gtfs_loader, self.trip_ids = route_ids, gtfs_loader, []
    def __call__(self) -> list[dtypes.Trip]: return self.build()
    def _call_trip_ids(self) -> list: return [row['trip_id'] for row in self.gtfs_loader.load(dload.LoadCSVFiles.TRIPS) if row['route_id'] in self.route_ids] 
    def _call_stop_ids(self) -> list: return [row['stop_id'] for row in self.gtfs_loader.load(dload.LoadCSVFiles.STOP_TIMES) if row['trip_id'] in self._call_trip_ids()]
    def build(self) -> list[dtypes.Trip]: return [dtypes.Trip(row['trip_id'], row['route_id'], row['direction_id'], StopBaseConstructor(self._call_stop_ids(), self.gtfs_loader).build(), StopTimeBaseConstructor(self._call_trip_ids(), self.gtfs_loader).build(), None) for row in self.gtfs_loader.load(dload.LoadCSVFiles.TRIPS) if row['route_id'] in self.route_ids]
         
class StopSequenceConstructor:
    def __int__(self, trip_id: dtypes.Trip, gtfs_loader: dload.BaseDataLoader) -> None: self.trip_id, self.gtfs_loader = trip_id, gtfs_loader
    def __call__(self) -> dict[dtypes.Stop: int]: return self.build()
    def build(self) -> dict[dtypes.Stop: int]: return {row['stop_id']: row['stop_sequence'] for row in self.gtfs_loader.load(dload.LoadCSVFiles.TRIPS) if row['trip_id'] in self.trip_id}

class RouteConstructor:
    def __init__(self, route_ids: list[dtypes.Route], gtfs_loader: dload.BaseDataLoader) -> None: self.route_ids, self.gtfs_loader = route_ids, gtfs_loader
    def __call__(self) -> list[dtypes.Route]: self.build()
    def build(self) -> list[dtypes.Route]: return [dtypes.Route(row['route_id'], row['agency_id'], row['route_short_name'], row['route_long_name'], row['route_type'], TripBaseConstructor(self.route_ids, self.gtfs_loader).build()) for row in self.gtfs_loader.load(dload.LoadCSVFiles.ROUTES) if row['route_id'] in self.route_ids]
         
class CorridorConstructor:
    def __init__(self, corridor_id: int, route_ids: list[dtypes.Route]) -> None: self.corridor_id, self.route_ids = corridor_id, route_ids
    def __call__(self) -> dtypes.Corridor: return self.build() 
    def build(self) -> dtypes.Corridor: return NotImplementedError #TODO: Implement this method

if __name__ == "__main__":
    loader = dload.GTFSLoadCSV('./data/agency.csv', './data/calendar.csv', './data/calendar_dates.csv', './data/routes.csv', './data/stop_times.csv', './data/stops.csv', './data/trips.csv')
    p = RouteConstructor(['2991_37732', '2990_40267'], loader).build()
    print(p[0])