from typing import Generator
import contextlib
import time

@contextlib.contextmanager
def timing(fnc_name: str) -> Generator[None, None, None]:
    t0 = time.monotonic()
    try: yield
    finally: print(f'LOG: {fnc_name} took {round(time.monotonic() - t0, 4)} SECONDS')

@contextlib.contextmanager
def vector_op(x: list[float], y: list[float]) -> list[float]:
    return NotImplementedError

@contextlib.contextmanager
def multithread_load_op() -> None:
    return NotImplementedError