"""
production_controller.py — Routes user menu choices to production view methods.

PoC scope: routing/coordination only. No business logic.
"""
from __future__ import annotations

from app.models.production_queue import ProductionQueue


class ProductionController:
    """Coordinates production sub-menu navigation and delegates display to the view."""

    def __init__(self, production_queue: ProductionQueue, view) -> None:
        self.production_queue = production_queue
        self.view = view

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def show_queue(self) -> None:
        """Extract all jobs from the queue (without dequeuing) and delegate to the view."""
        items = self.production_queue.snapshot()
        self.view.show_production_queue(items)

    def run(self) -> None:
        """Display the production sub-menu in a loop until the user selects 0."""
        while True:
            self.view.show_production_menu()
            choice = input("선택: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.show_queue()
