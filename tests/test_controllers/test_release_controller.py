"""
test_release_controller.py — TDD tests for ReleaseController.

RED phase: all tests are written before any production code exists.
"""
from unittest.mock import MagicMock, patch

import pytest

from app.models.order import Order, OrderStatus
from app.controllers.release_controller import ReleaseController


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def order_reserved():
    return Order("O001", "S001", "김철수", 100, OrderStatus.RESERVED)


@pytest.fixture
def order_producing():
    return Order("O002", "S001", "박민수", 50, OrderStatus.PRODUCING)


@pytest.fixture
def order_confirmed_a():
    return Order("O003", "S002", "이영희", 200, OrderStatus.CONFIRMED)


@pytest.fixture
def order_confirmed_b():
    return Order("O004", "S003", "최지훈", 150, OrderStatus.CONFIRMED)


@pytest.fixture
def order_released():
    return Order("O005", "S001", "정수연", 80, OrderStatus.RELEASE)


@pytest.fixture
def mock_view():
    return MagicMock()


# ---------------------------------------------------------------------------
# __init__ / construction
# ---------------------------------------------------------------------------

class TestReleaseControllerInit:
    def test_should_store_order_store_when_initialized(self, mock_view, order_confirmed_a):
        controller = ReleaseController(order_store=[order_confirmed_a], view=mock_view)

        assert controller.order_store == [order_confirmed_a]

    def test_should_store_view_when_initialized(self, mock_view):
        controller = ReleaseController(order_store=[], view=mock_view)

        assert controller.view is mock_view

    def test_should_accept_empty_order_store(self, mock_view):
        controller = ReleaseController(order_store=[], view=mock_view)

        assert controller.order_store == []


# ---------------------------------------------------------------------------
# list_confirmed_orders
# ---------------------------------------------------------------------------

class TestListConfirmedOrders:
    def test_should_pass_only_confirmed_orders_to_view(
        self, mock_view, order_reserved, order_confirmed_a
    ):
        controller = ReleaseController(
            order_store=[order_reserved, order_confirmed_a], view=mock_view
        )

        controller.list_confirmed_orders()

        mock_view.show_confirmed_orders.assert_called_once_with([order_confirmed_a])

    def test_should_pass_empty_list_when_no_confirmed_orders(
        self, mock_view, order_reserved, order_producing
    ):
        controller = ReleaseController(
            order_store=[order_reserved, order_producing], view=mock_view
        )

        controller.list_confirmed_orders()

        mock_view.show_confirmed_orders.assert_called_once_with([])

    def test_should_pass_all_confirmed_orders_when_multiple_exist(
        self, mock_view, order_confirmed_a, order_confirmed_b, order_reserved
    ):
        controller = ReleaseController(
            order_store=[order_confirmed_a, order_reserved, order_confirmed_b], view=mock_view
        )

        controller.list_confirmed_orders()

        mock_view.show_confirmed_orders.assert_called_once_with(
            [order_confirmed_a, order_confirmed_b]
        )

    def test_should_exclude_released_orders_from_confirmed_list(
        self, mock_view, order_confirmed_a, order_released
    ):
        controller = ReleaseController(
            order_store=[order_confirmed_a, order_released], view=mock_view
        )

        controller.list_confirmed_orders()

        args, _ = mock_view.show_confirmed_orders.call_args
        assert order_released not in args[0]
        assert order_confirmed_a in args[0]

    def test_should_exclude_reserved_orders_from_confirmed_list(
        self, mock_view, order_reserved, order_confirmed_a
    ):
        controller = ReleaseController(
            order_store=[order_reserved, order_confirmed_a], view=mock_view
        )

        controller.list_confirmed_orders()

        args, _ = mock_view.show_confirmed_orders.call_args
        assert order_reserved not in args[0]

    def test_should_pass_empty_list_when_order_store_is_empty(self, mock_view):
        controller = ReleaseController(order_store=[], view=mock_view)

        controller.list_confirmed_orders()

        mock_view.show_confirmed_orders.assert_called_once_with([])

    def test_should_not_call_any_other_view_method_when_list_confirmed_orders_called(
        self, mock_view, order_confirmed_a
    ):
        controller = ReleaseController(order_store=[order_confirmed_a], view=mock_view)

        controller.list_confirmed_orders()

        mock_view.show_release_menu.assert_not_called()


# ---------------------------------------------------------------------------
# run — menu loop
# ---------------------------------------------------------------------------

class TestRun:
    def test_should_show_release_menu_when_run_called(self, mock_view):
        with patch("builtins.input", return_value="0"):
            controller = ReleaseController(order_store=[], view=mock_view)
            controller.run()

        mock_view.show_release_menu.assert_called()

    def test_should_exit_loop_when_input_is_zero(self, mock_view):
        with patch("builtins.input", return_value="0"):
            controller = ReleaseController(order_store=[], view=mock_view)
            controller.run()

        assert True

    def test_should_call_show_confirmed_orders_when_input_is_one(
        self, mock_view, order_confirmed_a
    ):
        inputs = iter(["1", "0"])
        with patch("builtins.input", side_effect=inputs):
            controller = ReleaseController(order_store=[order_confirmed_a], view=mock_view)
            controller.run()

        mock_view.show_confirmed_orders.assert_called_once_with([order_confirmed_a])

    def test_should_pass_only_confirmed_orders_to_view_during_run(
        self, mock_view, order_confirmed_a, order_reserved
    ):
        inputs = iter(["1", "0"])
        with patch("builtins.input", side_effect=inputs):
            controller = ReleaseController(
                order_store=[order_confirmed_a, order_reserved], view=mock_view
            )
            controller.run()

        mock_view.show_confirmed_orders.assert_called_once_with([order_confirmed_a])

    def test_should_call_show_release_menu_on_each_iteration(self, mock_view):
        inputs = iter(["1", "0"])
        with patch("builtins.input", side_effect=inputs):
            controller = ReleaseController(order_store=[], view=mock_view)
            controller.run()

        assert mock_view.show_release_menu.call_count >= 2

    def test_should_handle_unknown_input_without_crashing(self, mock_view):
        inputs = iter(["9", "0"])
        with patch("builtins.input", side_effect=inputs):
            controller = ReleaseController(order_store=[], view=mock_view)
            controller.run()

        assert True
