"""
sample_controller.py — Routes user menu choices to sample view methods.

PoC scope: routing/coordination only. No business logic.
"""
from __future__ import annotations

from typing import List

from app.models.sample import Sample


class SampleController:
    """Coordinates sample sub-menu navigation and delegates display to the view."""

    def __init__(self, sample_store: List[Sample], view) -> None:
        self.sample_store = sample_store
        self.view = view

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_sample(self, sample: Sample) -> None:
        """Append a sample to the in-memory store."""
        self.sample_store.append(sample)

    def list_samples(self) -> None:
        """Delegate sample list rendering to the view."""
        self.view.show_sample_list(self.sample_store)

    def run(self) -> None:
        """Display the sample sub-menu in a loop until the user selects 0."""
        while True:
            self.view.show_sample_menu()
            choice = input("선택: ").strip()
            if choice == "0":
                break
            elif choice == "2":
                self.list_samples()
