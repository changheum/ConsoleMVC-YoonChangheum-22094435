"""
Tests for app/views/monitoring_view.py
TDD Phase 2 — View skeleton
"""
import pytest
from app.models.order import Order, OrderStatus
from app.models.inventory import Inventory
from app.views.monitoring_view import show_order_status_summary, show_inventory_status


class TestShowOrderStatusSummary:
    def test_should_print_reserved_count_when_given_orders(self, capsys):
        orders = [
            Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10,
                  status=OrderStatus.RESERVED),
            Order(order_id="O002", sample_id="S001", customer_name="김철수", quantity=5,
                  status=OrderStatus.RESERVED),
        ]
        show_order_status_summary(orders)
        captured = capsys.readouterr()
        assert "RESERVED" in captured.out
        assert "2" in captured.out

    def test_should_print_producing_count_when_given_orders(self, capsys):
        orders = [
            Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10,
                  status=OrderStatus.PRODUCING),
        ]
        show_order_status_summary(orders)
        captured = capsys.readouterr()
        assert "PRODUCING" in captured.out
        assert "1" in captured.out

    def test_should_print_confirmed_count_when_given_orders(self, capsys):
        orders = [
            Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10,
                  status=OrderStatus.CONFIRMED),
        ]
        show_order_status_summary(orders)
        captured = capsys.readouterr()
        assert "CONFIRMED" in captured.out
        assert "1" in captured.out

    def test_should_print_release_count_when_given_orders(self, capsys):
        orders = [
            Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10,
                  status=OrderStatus.RELEASE),
        ]
        show_order_status_summary(orders)
        captured = capsys.readouterr()
        assert "RELEASE" in captured.out
        assert "1" in captured.out

    def test_should_exclude_rejected_orders_when_given_mixed_orders(self, capsys):
        orders = [
            Order(order_id="O001", sample_id="S001", customer_name="홍길동", quantity=10,
                  status=OrderStatus.RESERVED),
            Order(order_id="O002", sample_id="S001", customer_name="김철수", quantity=5,
                  status=OrderStatus.REJECTED),
        ]
        show_order_status_summary(orders)
        captured = capsys.readouterr()
        assert "REJECTED" not in captured.out

    def test_should_print_zero_counts_when_given_empty_list(self, capsys):
        show_order_status_summary([])
        captured = capsys.readouterr()
        assert captured.out.strip() != ""
        assert "0" in captured.out

    def test_should_count_each_status_correctly_when_given_mixed_orders(self, capsys):
        orders = [
            Order(order_id="O001", sample_id="S001", customer_name="A", quantity=1,
                  status=OrderStatus.RESERVED),
            Order(order_id="O002", sample_id="S001", customer_name="B", quantity=1,
                  status=OrderStatus.PRODUCING),
            Order(order_id="O003", sample_id="S001", customer_name="C", quantity=1,
                  status=OrderStatus.REJECTED),  # Should be excluded
        ]
        show_order_status_summary(orders)
        captured = capsys.readouterr()
        assert "RESERVED" in captured.out
        assert "PRODUCING" in captured.out
        assert "REJECTED" not in captured.out


class TestShowInventoryStatus:
    def test_should_print_sample_id_when_given_inventory(self, capsys):
        inventories = [Inventory(sample_id="S001", quantity=100)]
        show_inventory_status(inventories)
        captured = capsys.readouterr()
        assert "S001" in captured.out

    def test_should_print_quantity_when_given_inventory(self, capsys):
        inventories = [Inventory(sample_id="S001", quantity=100)]
        show_inventory_status(inventories)
        captured = capsys.readouterr()
        assert "100" in captured.out

    def test_should_print_all_inventories_when_given_multiple(self, capsys):
        inventories = [
            Inventory(sample_id="S001", quantity=100),
            Inventory(sample_id="S002", quantity=50),
        ]
        show_inventory_status(inventories)
        captured = capsys.readouterr()
        assert "S001" in captured.out
        assert "S002" in captured.out
        assert "100" in captured.out
        assert "50" in captured.out

    def test_should_print_empty_message_when_given_empty_list(self, capsys):
        show_inventory_status([])
        captured = capsys.readouterr()
        assert captured.out.strip() != ""
        assert any(word in captured.out for word in ["없", "empty", "Empty", "0건", "없습니다"])
