import dtypes


class StopOps:
    def uclid_distance(stops: list[dtypes.Stop]) -> float: return NotImplementedError


class CorridorOps:
    def __init__(self, corridor: dtypes.Corridor) -> None: self.corridor = corridor
    def stop_frequency(self, start: float, end: float) -> list[float]: return NotImplementedError
    def build_timetable(self) -> ...:
