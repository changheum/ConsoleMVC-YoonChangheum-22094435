"""
Tests for app/views/main_menu_view.py
TDD Phase 2 — View skeleton
"""
import pytest
from app.views.main_menu_view import show_main_menu


class TestShowMainMenu:
    def test_should_print_item_1_sample_management_when_called(self, capsys):
        show_main_menu()
        captured = capsys.readouterr()
        assert "1" in captured.out
        assert "시료" in captured.out

    def test_should_print_item_2_order_when_called(self, capsys):
        show_main_menu()
        captured = capsys.readouterr()
        assert "2" in captured.out
        assert "주문" in captured.out

    def test_should_print_item_3_monitoring_when_called(self, capsys):
        show_main_menu()
        captured = capsys.readouterr()
        assert "3" in captured.out
        assert "모니터링" in captured.out

    def test_should_print_item_4_production_line_when_called(self, capsys):
        show_main_menu()
        captured = capsys.readouterr()
        assert "4" in captured.out
        assert "생산" in captured.out

    def test_should_print_item_5_release_when_called(self, capsys):
        show_main_menu()
        captured = capsys.readouterr()
        assert "5" in captured.out
        assert "출고" in captured.out

    def test_should_print_item_0_exit_when_called(self, capsys):
        show_main_menu()
        captured = capsys.readouterr()
        assert "0" in captured.out
        assert "종료" in captured.out

    def test_should_print_all_six_items_when_called(self, capsys):
        show_main_menu()
        captured = capsys.readouterr()
        for number in ["0", "1", "2", "3", "4", "5"]:
            assert number in captured.out
