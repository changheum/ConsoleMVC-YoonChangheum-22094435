"""
Tests for app/views/production_view.py
TDD Phase 2 — View skeleton
"""
import pytest
from app.models.production_queue import ProductionJob
from app.views.production_view import show_production_menu, show_production_queue


class TestShowProductionMenu:
    def test_should_print_start_production_option_when_called(self, capsys):
        show_production_menu()
        captured = capsys.readouterr()
        assert "1" in captured.out

    def test_should_print_view_queue_option_when_called(self, capsys):
        show_production_menu()
        captured = capsys.readouterr()
        assert "2" in captured.out

    def test_should_print_back_option_when_called(self, capsys):
        show_production_menu()
        captured = capsys.readouterr()
        assert "0" in captured.out

    def test_should_include_production_label_when_called(self, capsys):
        show_production_menu()
        captured = capsys.readouterr()
        assert "생산" in captured.out


class TestShowProductionQueue:
    def test_should_print_empty_message_when_given_empty_list(self, capsys):
        show_production_queue([])
        captured = capsys.readouterr()
        assert captured.out.strip() != ""
        assert any(word in captured.out for word in ["없", "empty", "Empty", "0건", "없습니다", "비어"])

    def test_should_print_order_id_when_given_one_job(self, capsys):
        job = ProductionJob(order_id="O001", sample_id="S001", required_quantity=10)
        show_production_queue([job])
        captured = capsys.readouterr()
        assert "O001" in captured.out

    def test_should_print_sample_id_when_given_one_job(self, capsys):
        job = ProductionJob(order_id="O001", sample_id="S001", required_quantity=10)
        show_production_queue([job])
        captured = capsys.readouterr()
        assert "S001" in captured.out

    def test_should_print_required_quantity_when_given_one_job(self, capsys):
        job = ProductionJob(order_id="O001", sample_id="S001", required_quantity=10)
        show_production_queue([job])
        captured = capsys.readouterr()
        assert "10" in captured.out

    def test_should_print_all_jobs_when_given_multiple_jobs(self, capsys):
        jobs = [
            ProductionJob(order_id="O001", sample_id="S001", required_quantity=10),
            ProductionJob(order_id="O002", sample_id="S002", required_quantity=20),
        ]
        show_production_queue(jobs)
        captured = capsys.readouterr()
        assert "O001" in captured.out
        assert "O002" in captured.out
        assert "S001" in captured.out
        assert "S002" in captured.out
