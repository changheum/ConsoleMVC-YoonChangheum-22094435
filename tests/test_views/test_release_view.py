"""
Tests for app/views/release_view.py
TDD Phase 2 — View skeleton
"""
import pytest
from app.models.order import Order, OrderStatus
from app.views.release_view import show_release_menu, show_confirmed_orders


class TestShowReleaseMenu:
    def test_should_print_process_release_option_when_called(self, capsys):
        show_release_menu()
        captured = capsys.readouterr()
        assert "1" in captured.out

    def test_should_print_back_option_when_called(self, capsys):
        show_release_menu()
        captured = capsys.readouterr()
        assert "0" in captured.out

    def test_should_include_release_label_when_called(self, capsys):
        show_release_menu()
        captured = capsys.readouterr()
        assert "출고" in captured.out


class TestShowConfirmedOrders:
    def test_should_print_empty_message_when_given_empty_list(self, capsys):
        show_confirmed_orders([])
        captured = capsys.readouterr()
        assert captured.out.strip() != ""
        assert any(word in captured.out for word in ["없", "empty", "Empty", "0건", "없습니다"])

    def test_should_print_order_id_when_given_confirmed_order(self, capsys):
        order = Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10,
                      status=OrderStatus.CONFIRMED)
        show_confirmed_orders([order])
        captured = capsys.readouterr()
        assert "O001" in captured.out

    def test_should_print_customer_name_when_given_confirmed_order(self, capsys):
        order = Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10,
                      status=OrderStatus.CONFIRMED)
        show_confirmed_orders([order])
        captured = capsys.readouterr()
        assert "홍길동" in captured.out

    def test_should_print_quantity_when_given_confirmed_order(self, capsys):
        order = Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10,
                      status=OrderStatus.CONFIRMED)
        show_confirmed_orders([order])
        captured = capsys.readouterr()
        assert "10" in captured.out

    def test_should_print_confirmed_status_when_given_confirmed_order(self, capsys):
        order = Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10,
                      status=OrderStatus.CONFIRMED)
        show_confirmed_orders([order])
        captured = capsys.readouterr()
        assert "CONFIRMED" in captured.out

    def test_should_print_all_confirmed_orders_when_given_multiple(self, capsys):
        orders = [
            Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10,
                  status=OrderStatus.CONFIRMED),
            Order(order_id="O002", sample_id="S002", customer_name="김철수", quantity=5,
                  status=OrderStatus.CONFIRMED),
        ]
        show_confirmed_orders(orders)
        captured = capsys.readouterr()
        assert "O001" in captured.out
        assert "O002" in captured.out
        assert "홍길동" in captured.out
        assert "김철수" in captured.out
