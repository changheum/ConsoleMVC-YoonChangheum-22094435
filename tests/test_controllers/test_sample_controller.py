"""
test_sample_controller.py — TDD tests for SampleController.

RED phase: all tests are written before any production code exists.
"""
from unittest.mock import MagicMock, call, patch

import pytest

from app.models.sample import Sample
from app.controllers.sample_controller import SampleController


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_a():
    return Sample("S001", "GaAs", 2.0, 0.9)


@pytest.fixture
def sample_b():
    return Sample("S002", "InP", 3.5, 0.85)


@pytest.fixture
def mock_view():
    return MagicMock()


# ---------------------------------------------------------------------------
# __init__ / construction
# ---------------------------------------------------------------------------

class TestSampleControllerInit:
    def test_should_store_sample_store_when_initialized(self, mock_view, sample_a):
        controller = SampleController(sample_store=[sample_a], view=mock_view)

        assert controller.sample_store == [sample_a]

    def test_should_store_view_when_initialized(self, mock_view):
        controller = SampleController(sample_store=[], view=mock_view)

        assert controller.view is mock_view

    def test_should_accept_empty_sample_store(self, mock_view):
        controller = SampleController(sample_store=[], view=mock_view)

        assert controller.sample_store == []


# ---------------------------------------------------------------------------
# add_sample
# ---------------------------------------------------------------------------

class TestAddSample:
    def test_should_add_sample_to_store_when_add_sample_called(self, mock_view, sample_a):
        controller = SampleController(sample_store=[], view=mock_view)

        controller.add_sample(sample_a)

        assert sample_a in controller.sample_store

    def test_should_increase_store_size_by_one_when_add_sample_called(self, mock_view, sample_a):
        controller = SampleController(sample_store=[], view=mock_view)

        controller.add_sample(sample_a)

        assert len(controller.sample_store) == 1

    def test_should_preserve_existing_samples_when_new_sample_added(self, mock_view, sample_a, sample_b):
        controller = SampleController(sample_store=[sample_a], view=mock_view)

        controller.add_sample(sample_b)

        assert sample_a in controller.sample_store
        assert sample_b in controller.sample_store

    def test_should_add_multiple_samples_sequentially(self, mock_view, sample_a, sample_b):
        controller = SampleController(sample_store=[], view=mock_view)

        controller.add_sample(sample_a)
        controller.add_sample(sample_b)

        assert controller.sample_store == [sample_a, sample_b]


# ---------------------------------------------------------------------------
# list_samples
# ---------------------------------------------------------------------------

class TestListSamples:
    def test_should_call_show_sample_list_when_list_samples_called(self, mock_view, sample_a):
        controller = SampleController(sample_store=[sample_a], view=mock_view)

        controller.list_samples()

        mock_view.show_sample_list.assert_called_once_with([sample_a])

    def test_should_pass_empty_list_to_view_when_store_is_empty(self, mock_view):
        controller = SampleController(sample_store=[], view=mock_view)

        controller.list_samples()

        mock_view.show_sample_list.assert_called_once_with([])

    def test_should_pass_all_samples_in_order_to_view(self, mock_view, sample_a, sample_b):
        controller = SampleController(sample_store=[sample_a, sample_b], view=mock_view)

        controller.list_samples()

        mock_view.show_sample_list.assert_called_once_with([sample_a, sample_b])

    def test_should_not_call_any_other_view_method_when_list_samples_called(self, mock_view, sample_a):
        controller = SampleController(sample_store=[sample_a], view=mock_view)

        controller.list_samples()

        mock_view.show_sample_menu.assert_not_called()
        mock_view.show_sample_detail.assert_not_called()


# ---------------------------------------------------------------------------
# run — menu loop
# ---------------------------------------------------------------------------

class TestRun:
    def test_should_show_sample_menu_when_run_called(self, mock_view):
        with patch("builtins.input", return_value="0"):
            controller = SampleController(sample_store=[], view=mock_view)
            controller.run()

        mock_view.show_sample_menu.assert_called()

    def test_should_exit_loop_when_input_is_zero(self, mock_view):
        with patch("builtins.input", return_value="0"):
            controller = SampleController(sample_store=[], view=mock_view)
            controller.run()  # must terminate, not loop forever

        # If we reach here the loop exited cleanly
        assert True

    def test_should_call_show_sample_list_when_input_is_one(self, mock_view, sample_a):
        inputs = iter(["1", "0"])
        with patch("builtins.input", side_effect=inputs):
            controller = SampleController(sample_store=[sample_a], view=mock_view)
            controller.run()

        mock_view.show_sample_list.assert_called_once_with([sample_a])

    def test_should_call_show_sample_menu_on_each_iteration(self, mock_view):
        inputs = iter(["1", "0"])
        with patch("builtins.input", side_effect=inputs):
            controller = SampleController(sample_store=[], view=mock_view)
            controller.run()

        # Menu shown at least twice (once for "1", once for "0")
        assert mock_view.show_sample_menu.call_count >= 2

    def test_should_handle_unknown_input_without_crashing(self, mock_view):
        inputs = iter(["9", "0"])
        with patch("builtins.input", side_effect=inputs):
            controller = SampleController(sample_store=[], view=mock_view)
            controller.run()

        assert True
