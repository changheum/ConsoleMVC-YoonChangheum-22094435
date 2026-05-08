"""
order_controller.py — Routes user menu choices to order view methods.

PoC scope: routing/coordination only. No business logic.
"""
from __future__ import annotations

from typing import List

from app.models.order import Order


class OrderController:
    """Coordinates order sub-menu navigation and delegates display to the view."""

    def __init__(self, order_store: List[Order], view) -> None:
        self.order_store = order_store
        self.view = view

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_order(self, order: Order) -> None:
        """Append an order to the in-memory store."""
        self.order_store.append(order)

    def list_orders(self) -> None:
        """Delegate order list rendering to the view."""
        self.view.show_order_list(self.order_store)

    def run(self) -> None:
        """Display the order sub-menu in a loop until the user selects 0."""
        while True:
            self.view.show_order_menu()
            choice = input("선택: ").strip()
            if choice == "0":
                break
            elif choice == "1":
                self.list_orders()
