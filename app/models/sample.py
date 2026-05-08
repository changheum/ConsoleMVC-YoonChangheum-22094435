"""
Sample model — data structure only.
No business logic, no console I/O.
"""
from dataclasses import dataclass


@dataclass
class Sample:
    sample_id: str
    name: str
    avg_production_time: float
    yield_rate: float
