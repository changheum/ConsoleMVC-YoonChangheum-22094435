"""
ProductionJob and ProductionQueue models — data structure and FIFO container only.
No business logic, no console I/O.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductionJob:
    order_id: str
    sample_id: str
    required_quantity: int


class ProductionQueue:
    """FIFO container for ProductionJob items.

    Scheduling strategy: First-In, First-Out (FIFO).
    This class is a pure data container — it holds no domain rules.
    """

    def __init__(self) -> None:
        self._queue: deque[ProductionJob] = deque()

    def enqueue(self, job: ProductionJob) -> None:
        """Add a job to the back of the queue."""
        self._queue.append(job)

    def dequeue(self) -> Optional[ProductionJob]:
        """Remove and return the front job. Returns None when the queue is empty."""
        if self.is_empty():
            return None
        return self._queue.popleft()

    def peek(self) -> Optional[ProductionJob]:
        """Return the front job without removing it. Returns None when the queue is empty."""
        if self.is_empty():
            return None
        return self._queue[0]

    def is_empty(self) -> bool:
        """Return True when the queue holds no jobs."""
        return len(self._queue) == 0

    def size(self) -> int:
        """Return the number of jobs currently in the queue."""
        return len(self._queue)

    def snapshot(self) -> list:
        """Return a shallow copy of all jobs in FIFO order without mutating the queue."""
        return list(self._queue)
