import dtypes



class CorridorOps:
    def __init__(self, corridor: dtypes.Corridor) -> None: self.corridor = corridor
    def stop_frequency(self, start: float, end: float, day_of_week: dtypes.ServiceTypes) -> list[float]: return NotImplementedError
    def build_timetable(self) -> ...: NotImplementedError