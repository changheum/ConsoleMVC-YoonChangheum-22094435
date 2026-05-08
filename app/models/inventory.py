"""
Inventory model — data structure only.
No business logic, no console I/O.
"""
from dataclasses import dataclass


@dataclass
class Inventory:
    sample_id: str
    quantity: int
