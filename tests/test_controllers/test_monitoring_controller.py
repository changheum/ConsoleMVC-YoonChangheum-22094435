"""
test_monitoring_controller.py — TDD tests for MonitoringController.

RED phase: all tests are written before any production code exists.
"""
from unittest.mock import MagicMock, patch

import pytest

from app.models.order import Order, OrderStatus
from app.models.inventory import Inventory
from app.controllers.monitoring_controller import MonitoringController


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def order_reserved():
    return Order("O001", "S001", "김철수", 100, OrderStatus.RESERVED)


@pytest.fixture
def order_confirmed():
    return Order("O002", "S002", "이영희", 200, OrderStatus.CONFIRMED)


@pytest.fixture
def inventory_a():
    return Inventory("S001", 500)


@pytest.fixture
def inventory_b():
    return Inventory("S002", 300)


@pytest.fixture
def mock_view():
    return MagicMock()


# ---------------------------------------------------------------------------
# __init__ / construction
# ---------------------------------------------------------------------------

class TestMonitoringControllerInit:
    def test_should_store_order_store_when_initialized(self, mock_view, order_reserved):
        controller = MonitoringController(
            order_store=[order_reserved],
            inventory_store=[],
            view=mock_view,
        )

        assert controller.order_store == [order_reserved]

    def test_should_store_inventory_store_when_initialized(self, mock_view, inventory_a):
        controller = MonitoringController(
            order_store=[],
            inventory_store=[inventory_a],
            view=mock_view,
        )

        assert controller.inventory_store == [inventory_a]

    def test_should_store_view_when_initialized(self, mock_view):
        controller = MonitoringController(order_store=[], inventory_store=[], view=mock_view)

        assert controller.view is mock_view

    def test_should_accept_empty_stores(self, mock_view):
        controller = MonitoringController(order_store=[], inventory_store=[], view=mock_view)

        assert controller.order_store == []
        assert controller.inventory_store == []


# ---------------------------------------------------------------------------
# show_summary
# ---------------------------------------------------------------------------

class TestShowSummary:
    def test_should_call_show_order_status_summary_with_order_store(
        self, mock_view, order_reserved, order_confirmed
    ):
        store = [order_reserved, order_confirmed]
        controller = MonitoringController(order_store=store, inventory_store=[], view=mock_view)

        controller.show_summary()

        mock_view.show_order_status_summary.assert_called_once_with(store)

    def test_should_pass_empty_list_to_summary_when_store_is_empty(self, mock_view):
        controller = MonitoringController(order_store=[], inventory_store=[], view=mock_view)

        controller.show_summary()

        mock_view.show_order_status_summary.assert_called_once_with([])

    def test_should_not_call_show_inventory_status_when_show_summary_called(
        self, mock_view, order_reserved
    ):
        controller = MonitoringController(
            order_store=[order_reserved], inventory_store=[], view=mock_view
        )

        controller.show_summary()

        mock_view.show_inventory_status.assert_not_called()


# ---------------------------------------------------------------------------
# show_inventory
# ---------------------------------------------------------------------------

class TestShowInventory:
    def test_should_call_show_inventory_status_with_inventory_store(
        self, mock_view, inventory_a, inventory_b
    ):
        store = [inventory_a, inventory_b]
        controller = MonitoringController(order_store=[], inventory_store=store, view=mock_view)

        controller.show_inventory()

        mock_view.show_inventory_status.assert_called_once_with(store)

    def test_should_pass_empty_list_to_inventory_view_when_store_is_empty(self, mock_view):
        controller = MonitoringController(order_store=[], inventory_store=[], view=mock_view)

        controller.show_inventory()

        mock_view.show_inventory_status.assert_called_once_with([])

    def test_should_not_call_show_order_status_summary_when_show_inventory_called(
        self, mock_view, inventory_a
    ):
        controller = MonitoringController(
            order_store=[], inventory_store=[inventory_a], view=mock_view
        )

        controller.show_inventory()

        mock_view.show_order_status_summary.assert_not_called()


# ---------------------------------------------------------------------------
# run — shows both summary and inventory
# ---------------------------------------------------------------------------

class TestRun:
    def test_should_call_show_order_status_summary_when_run_called(
        self, mock_view, order_reserved
    ):
        controller = MonitoringController(
            order_store=[order_reserved], inventory_store=[], view=mock_view
        )

        controller.run()

        mock_view.show_order_status_summary.assert_called_once_with([order_reserved])

    def test_should_call_show_inventory_status_when_run_called(
        self, mock_view, inventory_a
    ):
        controller = MonitoringController(
            order_store=[], inventory_store=[inventory_a], view=mock_view
        )

        controller.run()

        mock_view.show_inventory_status.assert_called_once_with([inventory_a])

    def test_should_call_both_view_methods_when_run_called(
        self, mock_view, order_reserved, inventory_a
    ):
        controller = MonitoringController(
            order_store=[order_reserved],
            inventory_store=[inventory_a],
            view=mock_view,
        )

        controller.run()

        mock_view.show_order_status_summary.assert_called_once_with([order_reserved])
        mock_view.show_inventory_status.assert_called_once_with([inventory_a])
