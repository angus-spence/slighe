import os
import csv
from dataclasses import dataclass
from enum import Enum

class GTFSLoadMethod(Enum):
    from_csv = 1
    from_postgres = 2
    from_sqlite = 3
    from_transxchange = 4

@dataclass
class BaseDataLoader: 
    load_method: GTFSLoadMethod

class GTFSLoadCSV(BaseDataLoader):
    def __init__(self, agency_path: str, calendar_path: str, calendar_dates_path: str, routes_path: str, stop_times_path: str, stops_path: str, trips_path: str) -> None:
        super().__init__(GTFSLoadMethod.from_csv)
        self.agency_path = agency_path
        self.calendar_path = calendar_path
        self.calendar_dates_path = calendar_dates_path
        self.routes_path = routes_path
        self.stop_times_path = stop_times_path
        self.stops_path = stops_path
        self.trips_path = trips_path
        if not self._validate_paths(): raise FileNotFoundError('One or more paths do not exist') 
        self.paths = [path for path in self.__dict__.values() if str(path).endswith('.csv')]
        self.agency = self._agency_load()
        self.calendar = self._calendar_load()
        self.calendar_dates = self._calendar_dates_load()
        self.routes = self._routes_load()
        self.stop_times = self._stop_times_load()
        self.stops = self._stops_load()
        self.trips = self._trips_load()
    def __call__(self) -> None: self.load()
    def _validate_paths(self) -> None: return all([os.path.exists(path) for path in self.__dict__.values() if str(path).endswith('.csv')])
    def _agency_load(self) -> csv.DictReader: return self._load_csv(self.agency_path)
    def _calendar_load(self) -> csv.DictReader: return self._load_csv(self.calendar_path)
    def _calendar_dates_load(self) -> csv.DictReader: return self._load_csv(self.calendar_dates_path)
    def _routes_load(self) -> csv.DictReader: return self._load_csv(self.routes_path)
    def _stop_times_load(self) -> csv.DictReader: return self._load_csv(self.stop_times_path)
    def _stops_load(self) -> csv.DictReader: return self._load_csv(self.stops_path)
    def _trips_load(self) -> csv.DictReader: return self._load_csv(self.trips_path)
    def _load_csv(self, path: str) -> csv.DictReader:
        with open(path, 'r') as csv_file: return csv.DictReader(csv_file)

    





if __name__ == "__main__":
    gtfs_loader = GTFSLoadCSV('./data/agency.csv', './data/calendar.csv', './data/calendar_dates.csv', './data/routes.csv', './data/stop_times.csv', './data/stops.csv', './data/trips.csv')
    print(gtfs_loader.paths)
    #print(gtfs_loader.paths)