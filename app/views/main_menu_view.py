"""
main_menu_view.py — Main menu rendering.
Console output only: no input(), no business logic.
"""
from app.views.base_view import print_header


def show_main_menu() -> None:
    """Print the main menu options to stdout."""
    print_header("메인 메뉴")
    print("1. 시료 관리")
    print("2. 주문 (접수 / 승인 / 거절)")
    print("3. 모니터링")
    print("4. 생산 라인")
    print("5. 출고 처리")
    print("0. 종료")
