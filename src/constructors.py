import dtypes

import csv

class StopBaseConstructor:
    def __init__(self, stop_ids: list[dtypes.Stop.stop_id], stop_csv_path: str) -> None: self.stop_ids = stop_ids; self.stop_csv_path = stop_csv_path
    def __call__(self) -> list[dtypes.Stop]: self._load_from_csv()
    def _load_from_csv(self) -> list[dtypes.Stop]:
        with open(self.stop_csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            return [dtypes.Stop(row['stop_id'], row['stop_name'], row['stop_lat'], row['stop_lon'], row['settlement'], row['country']) for row in reader if row['stop_id'] in self.stop_ids]

class StopTimeBaseConstructor:
    def __init__(self, trip_id: dtypes.Trip.trip_id, stop_times_csv_path: str) -> None: self.trip_id = trip_id; self.stop_times_csv_path = stop_times_csv_path
    def __call__(self) -> list[dtypes.StopTime]: self._load_from_csv()
    def _load_from_csv(self) -> list[dtypes.StopTime]:
        with open(self.stop_times_csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            return [dtypes.Stop(row['stop_id'], row['arrival_time'], row['departure_time']) for row in reader if row['trip_id'] in self.trip_id]

class TripBaseConstructor:
    def __init__(self, route_ids: list[dtypes.Route.route_id], trip_csv_path: str, stop_csv_path: str) -> None: self.route_ids = route_ids; self.trip_csv_path = trip_csv_path; self.stop_csv_path = stop_csv_path
    def __call__(self) -> list[dtypes.Trip]: self._load_from_csv()
    def _collect_stops(self, reader: csv.DictReader) -> list: return [row['stop_id'] for row in reader]
    def _collect_trips(self, reader: csv.DictReader) -> list[dtypes.Trip]: return [row['trip_id'] for row in reader if row['trip_id'] in self.route_ids]
    def _load_from_csv(self) -> list[dtypes.Trip]:
        with open(self.trip_csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            return [dtypes.Trip(row['trip_id'], 
                                row['route_id'], 
                                StopBaseConstructor(self._collect_stops(reader), self.stop_csv_path), 
                                StopTimeBaseConstructor(self._collect_trips(reader, self.stop_csv_path)),
                                StopSequenceConstructor(self._collect_trips(reader, self.stop_csv_path)))
                                for row in reader if row['route_id'] in self.route_ids]

class StopSequenceConstructor:
    def __int__(self, trip_id: dtypes.Trip.trip_id, stop_times_csv_path: str) -> None: self.trip_id = trip_id; self.stop_times_csv_path = stop_times_csv_path
    def __call__(self) -> dict[dtypes.Stop.stop_id: int]: return self._load_from_csv()
    def _load_from_csv(self) -> dict[dtypes.Stop.stop_id, int]:
        with open(self.stop_times_csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            return {row['stop_id']: row['stop_sequence'] for row in reader if row['trip_id'] in self.trip_id}

class RouteConstructor:
    def __init__(self, route_ids: list[dtypes.Route.route_id], route_csv_path: str) -> None: self.route_ids = route_ids; self.route_csv_path = route_csv_path
    def __call__(self) -> list[dtypes.Route]: self._load_from_csv()
    def _load_from_csv(self) -> list[dtypes.Route]:
        with open(self.route_csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            return [dtypes.Route(row['route_id'], row['agency_id'], row['route_short_name'], row['route_long_name'])]

    def build_from_csv(self, corridor_services_csv_path: str) -> ...:
        services = []
        with open(corridor_services_csv_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['corridor_id'] == self.corridor_id:
                    services.append([row['route_id'], row['route_short_name']])
        
    def _load_gtfs_stops_csv(self, stops_file_path: str) -> list[Stop]:
        with open(stops_file_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.stops.append(Stop(
                    stop_id=row['stop_id'],
                    stop_name=row['stop_name'],
                    stop_latitude=row['stop_lat'],
                    stop_longitude=row['stop_lon'],
                    settlement=row['settlement'],
                    county=row['county'],
                    service_type=None
                ))
        return self.stops
    
    def _load_services(self, services_file_path: str, corridor_services: list = None) -> list[Route]:
        with open(services_file_path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if corridor_services and row['route_id'] in corridor_services:
                    self.routes.append(Route(
                        route_id=row['route_id'],
                        agency_id=row['agency_id'],
                        route_short_name=row['route_short_name'],
                        route_long_name=row['route_long_name'],
                        route_type=row['route_type'],
                        stops=None,
                        stop_sequence=None,
                        stop_times=None,
                        service_type=None
                    ))
                else: raise ValueError(f'No corridor_services specified, or services not in corridor')
        return