"""
Tests for app/views/order_view.py
TDD Phase 2 — View skeleton
"""
import pytest
from app.models.order import Order, OrderStatus
from app.views.order_view import show_order_menu, show_order_list


class TestShowOrderMenu:
    def test_should_print_receive_option_when_called(self, capsys):
        show_order_menu()
        captured = capsys.readouterr()
        assert "1" in captured.out

    def test_should_print_approve_option_when_called(self, capsys):
        show_order_menu()
        captured = capsys.readouterr()
        assert "2" in captured.out

    def test_should_print_reject_option_when_called(self, capsys):
        show_order_menu()
        captured = capsys.readouterr()
        assert "3" in captured.out

    def test_should_print_back_option_when_called(self, capsys):
        show_order_menu()
        captured = capsys.readouterr()
        assert "0" in captured.out

    def test_should_include_order_label_when_called(self, capsys):
        show_order_menu()
        captured = capsys.readouterr()
        assert "주문" in captured.out


class TestShowOrderList:
    def test_should_print_empty_message_when_given_empty_list(self, capsys):
        show_order_list([])
        captured = capsys.readouterr()
        assert captured.out.strip() != ""
        assert any(word in captured.out for word in ["없", "empty", "Empty", "0건", "없습니다"])

    def test_should_print_order_id_when_given_one_order(self, capsys):
        order = Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10)
        show_order_list([order])
        captured = capsys.readouterr()
        assert "O001" in captured.out

    def test_should_print_customer_name_when_given_one_order(self, capsys):
        order = Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10)
        show_order_list([order])
        captured = capsys.readouterr()
        assert "홍길동" in captured.out

    def test_should_print_quantity_when_given_one_order(self, capsys):
        order = Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10)
        show_order_list([order])
        captured = capsys.readouterr()
        assert "10" in captured.out

    def test_should_print_status_when_given_one_order(self, capsys):
        order = Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10,
                      status=OrderStatus.RESERVED)
        show_order_list([order])
        captured = capsys.readouterr()
        assert "RESERVED" in captured.out

    def test_should_print_all_orders_when_given_multiple_orders(self, capsys):
        orders = [
            Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10),
            Order(order_id="O002", sample_id="S002", customer_name="김철수", quantity=5),
        ]
        show_order_list(orders)
        captured = capsys.readouterr()
        assert "O001" in captured.out
        assert "O002" in captured.out
        assert "홍길동" in captured.out
        assert "김철수" in captured.out
