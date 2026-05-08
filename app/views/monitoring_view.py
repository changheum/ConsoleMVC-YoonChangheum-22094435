"""
monitoring_view.py — Monitoring / status dashboard rendering.
Console output only: no input(), no business logic.
"""
from __future__ import annotations

from typing import List

from app.models.inventory import Inventory
from app.models.order import Order, OrderStatus
from app.views.base_view import print_header, print_separator

# Statuses shown in the summary (REJECTED is intentionally excluded per PRD)
_SUMMARY_STATUSES = [
    OrderStatus.RESERVED,
    OrderStatus.PRODUCING,
    OrderStatus.CONFIRMED,
    OrderStatus.RELEASE,
]


def show_order_status_summary(orders: List[Order]) -> None:
    """Print a count of orders grouped by status, excluding REJECTED."""
    print_header("주문 현황 요약")
    counts = {status: 0 for status in _SUMMARY_STATUSES}
    for order in orders:
        if order.status in counts:
            counts[order.status] += 1
    for status in _SUMMARY_STATUSES:
        print(f"{status.value:<12}: {counts[status]}건")


def show_inventory_status(inventories: List[Inventory]) -> None:
    """Print the current inventory levels for all samples."""
    print_header("재고 현황")
    if not inventories:
        print("등록된 재고가 없습니다.")
        return
    print(f"{'시료ID':<12} {'수량':>8}")
    print_separator()
    for inv in inventories:
        print(f"{inv.sample_id:<12} {inv.quantity:>8}")
