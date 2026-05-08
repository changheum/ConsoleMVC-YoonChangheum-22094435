"""
test_order_controller.py — TDD tests for OrderController.

RED phase: all tests are written before any production code exists.
"""
from unittest.mock import MagicMock, patch

import pytest

from app.models.order import Order, OrderStatus
from app.controllers.order_controller import OrderController


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def order_a():
    return Order("O001", "S001", "김철수", 100)


@pytest.fixture
def order_b():
    return Order("O002", "S002", "이영희", 200, OrderStatus.CONFIRMED)


@pytest.fixture
def mock_view():
    return MagicMock()


# ---------------------------------------------------------------------------
# __init__ / construction
# ---------------------------------------------------------------------------

class TestOrderControllerInit:
    def test_should_store_order_store_when_initialized(self, mock_view, order_a):
        controller = OrderController(order_store=[order_a], view=mock_view)

        assert controller.order_store == [order_a]

    def test_should_store_view_when_initialized(self, mock_view):
        controller = OrderController(order_store=[], view=mock_view)

        assert controller.view is mock_view

    def test_should_accept_empty_order_store(self, mock_view):
        controller = OrderController(order_store=[], view=mock_view)

        assert controller.order_store == []


# ---------------------------------------------------------------------------
# add_order
# ---------------------------------------------------------------------------

class TestAddOrder:
    def test_should_add_order_to_store_when_add_order_called(self, mock_view, order_a):
        controller = OrderController(order_store=[], view=mock_view)

        controller.add_order(order_a)

        assert order_a in controller.order_store

    def test_should_increase_store_size_by_one_when_add_order_called(self, mock_view, order_a):
        controller = OrderController(order_store=[], view=mock_view)

        controller.add_order(order_a)

        assert len(controller.order_store) == 1

    def test_should_preserve_existing_orders_when_new_order_added(self, mock_view, order_a, order_b):
        controller = OrderController(order_store=[order_a], view=mock_view)

        controller.add_order(order_b)

        assert order_a in controller.order_store
        assert order_b in controller.order_store

    def test_should_add_multiple_orders_sequentially(self, mock_view, order_a, order_b):
        controller = OrderController(order_store=[], view=mock_view)

        controller.add_order(order_a)
        controller.add_order(order_b)

        assert controller.order_store == [order_a, order_b]


# ---------------------------------------------------------------------------
# list_orders
# ---------------------------------------------------------------------------

class TestListOrders:
    def test_should_call_show_order_list_when_list_orders_called(self, mock_view, order_a):
        controller = OrderController(order_store=[order_a], view=mock_view)

        controller.list_orders()

        mock_view.show_order_list.assert_called_once_with([order_a])

    def test_should_pass_empty_list_to_view_when_store_is_empty(self, mock_view):
        controller = OrderController(order_store=[], view=mock_view)

        controller.list_orders()

        mock_view.show_order_list.assert_called_once_with([])

    def test_should_pass_all_orders_in_order_to_view(self, mock_view, order_a, order_b):
        controller = OrderController(order_store=[order_a, order_b], view=mock_view)

        controller.list_orders()

        mock_view.show_order_list.assert_called_once_with([order_a, order_b])

    def test_should_not_call_show_order_menu_when_list_orders_called(self, mock_view, order_a):
        controller = OrderController(order_store=[order_a], view=mock_view)

        controller.list_orders()

        mock_view.show_order_menu.assert_not_called()


# ---------------------------------------------------------------------------
# run — menu loop
# ---------------------------------------------------------------------------

class TestRun:
    def test_should_show_order_menu_when_run_called(self, mock_view):
        with patch("builtins.input", return_value="0"):
            controller = OrderController(order_store=[], view=mock_view)
            controller.run()

        mock_view.show_order_menu.assert_called()

    def test_should_exit_loop_when_input_is_zero(self, mock_view):
        with patch("builtins.input", return_value="0"):
            controller = OrderController(order_store=[], view=mock_view)
            controller.run()

        assert True

    def test_should_call_show_order_list_when_input_is_one(self, mock_view, order_a):
        inputs = iter(["1", "0"])
        with patch("builtins.input", side_effect=inputs):
            controller = OrderController(order_store=[order_a], view=mock_view)
            controller.run()

        mock_view.show_order_list.assert_called_once_with([order_a])

    def test_should_call_show_order_menu_on_each_iteration(self, mock_view):
        inputs = iter(["1", "0"])
        with patch("builtins.input", side_effect=inputs):
            controller = OrderController(order_store=[], view=mock_view)
            controller.run()

        assert mock_view.show_order_menu.call_count >= 2

    def test_should_handle_unknown_input_without_crashing(self, mock_view):
        inputs = iter(["9", "0"])
        with patch("builtins.input", side_effect=inputs):
            controller = OrderController(order_store=[], view=mock_view)
            controller.run()

        assert True
