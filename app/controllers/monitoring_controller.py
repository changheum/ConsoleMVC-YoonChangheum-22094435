"""
monitoring_controller.py — Coordinates monitoring/dashboard display.

PoC scope: routing/coordination only. No business logic.
"""
from __future__ import annotations

from typing import List

from app.models.order import Order
from app.models.inventory import Inventory


class MonitoringController:
    """Coordinates the monitoring dashboard view — no sub-menu loop needed."""

    def __init__(self, order_store: List[Order], inventory_store: List[Inventory], view) -> None:
        self.order_store = order_store
        self.inventory_store = inventory_store
        self.view = view

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def show_summary(self) -> None:
        """Delegate order status summary rendering to the view."""
        self.view.show_order_status_summary(self.order_store)

    def show_inventory(self) -> None:
        """Delegate inventory status rendering to the view."""
        self.view.show_inventory_status(self.inventory_store)

    def run(self) -> None:
        """Display both monitoring panels in sequence."""
        self.show_summary()
        self.show_inventory()
