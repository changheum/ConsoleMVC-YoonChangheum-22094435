"""
release_controller.py — Routes user menu choices to release view methods.

PoC scope: routing/coordination only. No business logic.
"""
from __future__ import annotations

from typing import List

from app.models.order import Order, OrderStatus


class ReleaseController:
    """Coordinates release sub-menu navigation and delegates display to the view."""

    def __init__(self, order_store: List[Order], view) -> None:
        self.order_store = order_store
        self.view = view

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def list_confirmed_orders(self) -> None:
        """Filter CONFIRMED orders from the store and delegate rendering to the view."""
        confirmed = [o for o in self.order_store if o.status == OrderStatus.CONFIRMED]
        self.view.show_confirmed_orders(confirmed)

    def run(self) -> None:
        """Display the release sub-menu in a loop until the user selects 0."""
        while True:
            self.view.show_release_menu()
            choice = input("선택: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.list_confirmed_orders()
