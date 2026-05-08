"""
test_production_controller.py — TDD tests for ProductionController.

RED phase: all tests are written before any production code exists.
"""
from unittest.mock import MagicMock, patch

import pytest

from app.models.production_queue import ProductionJob, ProductionQueue
from app.controllers.production_controller import ProductionController


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def job_a():
    return ProductionJob("O001", "S001", 100)


@pytest.fixture
def job_b():
    return ProductionJob("O002", "S002", 200)


@pytest.fixture
def empty_queue():
    return ProductionQueue()


@pytest.fixture
def queue_with_one_job(job_a):
    q = ProductionQueue()
    q.enqueue(job_a)
    return q


@pytest.fixture
def queue_with_two_jobs(job_a, job_b):
    q = ProductionQueue()
    q.enqueue(job_a)
    q.enqueue(job_b)
    return q


@pytest.fixture
def mock_view():
    return MagicMock()


# ---------------------------------------------------------------------------
# __init__ / construction
# ---------------------------------------------------------------------------

class TestProductionControllerInit:
    def test_should_store_production_queue_when_initialized(self, mock_view, queue_with_one_job):
        controller = ProductionController(production_queue=queue_with_one_job, view=mock_view)

        assert controller.production_queue is queue_with_one_job

    def test_should_store_view_when_initialized(self, mock_view, empty_queue):
        controller = ProductionController(production_queue=empty_queue, view=mock_view)

        assert controller.view is mock_view

    def test_should_accept_empty_queue(self, mock_view, empty_queue):
        controller = ProductionController(production_queue=empty_queue, view=mock_view)

        assert controller.production_queue.is_empty()


# ---------------------------------------------------------------------------
# show_queue
# ---------------------------------------------------------------------------

class TestShowQueue:
    def test_should_call_show_production_queue_with_empty_list_when_queue_is_empty(
        self, mock_view, empty_queue
    ):
        controller = ProductionController(production_queue=empty_queue, view=mock_view)

        controller.show_queue()

        mock_view.show_production_queue.assert_called_once_with([])

    def test_should_call_show_production_queue_with_all_jobs_when_queue_has_items(
        self, mock_view, queue_with_two_jobs, job_a, job_b
    ):
        controller = ProductionController(production_queue=queue_with_two_jobs, view=mock_view)

        controller.show_queue()

        mock_view.show_production_queue.assert_called_once_with([job_a, job_b])

    def test_should_call_show_production_queue_with_single_job_when_queue_has_one_item(
        self, mock_view, queue_with_one_job, job_a
    ):
        controller = ProductionController(production_queue=queue_with_one_job, view=mock_view)

        controller.show_queue()

        mock_view.show_production_queue.assert_called_once_with([job_a])

    def test_should_not_dequeue_items_when_show_queue_called(
        self, mock_view, queue_with_two_jobs
    ):
        controller = ProductionController(production_queue=queue_with_two_jobs, view=mock_view)

        controller.show_queue()

        # Queue must remain intact after display
        assert queue_with_two_jobs.size() == 2

    def test_should_preserve_queue_order_when_show_queue_called(
        self, mock_view, queue_with_two_jobs, job_a, job_b
    ):
        controller = ProductionController(production_queue=queue_with_two_jobs, view=mock_view)

        controller.show_queue()

        args, _ = mock_view.show_production_queue.call_args
        assert args[0] == [job_a, job_b]


# ---------------------------------------------------------------------------
# run — menu loop
# ---------------------------------------------------------------------------

class TestRun:
    def test_should_show_production_menu_when_run_called(self, mock_view, empty_queue):
        with patch("builtins.input", return_value="0"):
            controller = ProductionController(production_queue=empty_queue, view=mock_view)
            controller.run()

        mock_view.show_production_menu.assert_called()

    def test_should_exit_loop_when_input_is_zero(self, mock_view, empty_queue):
        with patch("builtins.input", return_value="0"):
            controller = ProductionController(production_queue=empty_queue, view=mock_view)
            controller.run()

        assert True

    def test_should_call_show_production_queue_when_input_is_one(
        self, mock_view, queue_with_one_job, job_a
    ):
        inputs = iter(["1", "0"])
        with patch("builtins.input", side_effect=inputs):
            controller = ProductionController(production_queue=queue_with_one_job, view=mock_view)
            controller.run()

        mock_view.show_production_queue.assert_called_once_with([job_a])

    def test_should_call_show_production_menu_on_each_iteration(self, mock_view, empty_queue):
        inputs = iter(["1", "0"])
        with patch("builtins.input", side_effect=inputs):
            controller = ProductionController(production_queue=empty_queue, view=mock_view)
            controller.run()

        assert mock_view.show_production_menu.call_count >= 2

    def test_should_handle_unknown_input_without_crashing(self, mock_view, empty_queue):
        inputs = iter(["9", "0"])
        with patch("builtins.input", side_effect=inputs):
            controller = ProductionController(production_queue=empty_queue, view=mock_view)
            controller.run()

        assert True
