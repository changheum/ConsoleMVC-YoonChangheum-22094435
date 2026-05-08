"""
release_view.py — Release / shipment processing rendering.
Console output only: no input(), no business logic.
"""
from __future__ import annotations

from typing import List

from app.models.order import Order
from app.views.base_view import print_header, print_separator


def show_release_menu() -> None:
    """Print the release processing sub-menu options."""
    print_header("출고 처리")
    print("1. 출고 처리")
    print("0. 뒤로")


def show_confirmed_orders(orders: List[Order]) -> None:
    """Print orders that are in CONFIRMED status and ready for release."""
    print_header("출고 대기 주문")
    if not orders:
        print("출고 대기 중인 주문이 없습니다.")
        return
    print(f"{'주문ID':<10} {'시료ID':<10} {'고객명':<12} {'수량':>6} {'상태':<12}")
    print_separator()
    for order in orders:
        print(
            f"{order.order_id:<10} {order.sample_id:<10} {order.customer_name:<12} "
            f"{order.quantity:>6} {order.status.value:<12}"
        )
