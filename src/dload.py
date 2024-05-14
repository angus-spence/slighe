import dtypes

import os
import csv
from dataclasses import dataclass
from enum import Enum
from typing import overload

class GTFSLoadMethod(Enum):
    from_csv = 1
    from_postgres = 2
    from_sqlite = 3
    from_transxchange = 4

class LoadCSVFiles(Enum):
    AGENCY = 1
    CALENDAR = 2
    CALENDAR_DATES = 3
    ROUTES = 4
    STOP_TIMES = 5
    STOPS = 6
    TRIPS = 7

@dataclass
class BaseDataLoader: 
    load_method: GTFSLoadMethod

    @overload
    def load(self, file: LoadCSVFiles) -> csv.DictReader: ...

class GTFSLoadCSV(BaseDataLoader):
    def __init__(self, agency_path: str, calendar_path: str, calendar_dates_path: str, routes_path: str, stop_times_path: str, stops_path: str, trips_path: str) -> None:
        super().__init__(GTFSLoadMethod.from_csv)
        self.agency_path, self.calendar_path, self.calendar_dates_path, self.routes_path, self.stop_times_path, self.stops_path, self.trips_path = agency_path, calendar_path, calendar_dates_path, routes_path, stop_times_path, stops_path, trips_path
        if not self._validate_paths(): raise FileNotFoundError('One or more paths do not exist') 
        self.paths = {file: path for file, path in zip(LoadCSVFiles, self.__dict__.values()) if str(path).endswith('.csv')}
        
        # TODO: LOAD CSV FILES TO MEMORY FOR NOW -> WE WOULD PREFER TO OPEN ONCE AND READ ONLY REQUIRED

    def __call__(self, file: LoadCSVFiles) -> None: self.load(file)
    
    def _validate_paths(self) -> bool: return all([os.path.exists(path) for path in self.__dict__.values() if str(path).endswith('.csv')])

    def load(self, file: LoadCSVFiles) -> csv.DictReader:
        return self.csv_files[file]

if __name__ == "__main__":
    gtfs_loader = GTFSLoadCSV('./data/agency.csv', './data/calendar.csv', './data/calendar_dates.csv', './data/routes.csv', './data/stop_times.csv', './data/stops.csv', './data/trips.csv')