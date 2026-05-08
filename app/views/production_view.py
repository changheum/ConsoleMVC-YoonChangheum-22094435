"""
production_view.py — Production line rendering.
Console output only: no input(), no business logic.
"""
from __future__ import annotations

from typing import List

from app.models.production_queue import ProductionJob
from app.views.base_view import print_header, print_separator


def show_production_menu() -> None:
    """Print the production line sub-menu options."""
    print_header("생산 라인")
    print("1. 생산 시작")
    print("2. 생산 대기열 조회")
    print("0. 뒤로")


def show_production_queue(queue_items: List[ProductionJob]) -> None:
    """Print the list of pending production jobs."""
    print_header("생산 대기열")
    if not queue_items:
        print("대기 중인 생산 작업이 없습니다.")
        return
    print(f"{'주문ID':<10} {'시료ID':<10} {'요구수량':>8}")
    print_separator()
    for idx, job in enumerate(queue_items, start=1):
        print(f"{job.order_id:<10} {job.sample_id:<10} {job.required_quantity:>8}")
