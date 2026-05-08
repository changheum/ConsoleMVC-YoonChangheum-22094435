"""
order_view.py — Order management rendering.
Console output only: no input(), no business logic.
"""
from __future__ import annotations

from typing import List

from app.models.order import Order
from app.views.base_view import print_header, print_separator


def show_order_menu() -> None:
    """Print the order management sub-menu options."""
    print_header("주문 관리")
    print("1. 주문 접수")
    print("2. 주문 승인")
    print("3. 주문 거절")
    print("0. 뒤로")


def show_order_list(orders: List[Order]) -> None:
    """Print a list of orders. Prints an empty-list message when the list is empty."""
    print_header("주문 목록")
    if not orders:
        print("등록된 주문이 없습니다.")
        return
    print(f"{'주문ID':<10} {'시료ID':<10} {'고객명':<12} {'수량':>6} {'상태':<12}")
    print_separator()
    for order in orders:
        print(
            f"{order.order_id:<10} {order.sample_id:<10} {order.customer_name:<12} "
            f"{order.quantity:>6} {order.status.value:<12}"
        )
