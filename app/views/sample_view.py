"""
sample_view.py — Sample management rendering.
Console output only: no input(), no business logic.
"""
from __future__ import annotations

from typing import List

from app.models.sample import Sample
from app.views.base_view import print_header, print_separator


def show_sample_menu() -> None:
    """Print the sample management sub-menu options."""
    print_header("시료 관리")
    print("1. 시료 등록")
    print("2. 시료 목록 조회")
    print("0. 뒤로")


def show_sample_list(samples: List[Sample]) -> None:
    """Print a list of samples. Prints an empty-list message when the list is empty."""
    print_header("시료 목록")
    if not samples:
        print("등록된 시료가 없습니다.")
        return
    print(f"{'ID':<10} {'이름':<15} {'평균생산시간':>12} {'수율':>8}")
    print_separator()
    for sample in samples:
        print(f"{sample.sample_id:<10} {sample.name:<15} {sample.avg_production_time:>12} {sample.yield_rate:>8}")


def show_sample_detail(sample: Sample) -> None:
    """Print the detail view for a single sample."""
    print_header("시료 상세")
    print(f"시료 ID      : {sample.sample_id}")
    print(f"이름         : {sample.name}")
    print(f"평균 생산시간: {sample.avg_production_time}")
    print(f"수율         : {sample.yield_rate}")
