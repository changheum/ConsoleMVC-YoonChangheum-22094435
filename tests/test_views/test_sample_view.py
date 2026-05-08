"""
Tests for app/views/sample_view.py
TDD Phase 2 — View skeleton
"""
import pytest
from app.models.sample import Sample
from app.views.sample_view import show_sample_menu, show_sample_list, show_sample_detail


class TestShowSampleMenu:
    def test_should_print_add_option_when_called(self, capsys):
        show_sample_menu()
        captured = capsys.readouterr()
        assert "1" in captured.out

    def test_should_print_list_option_when_called(self, capsys):
        show_sample_menu()
        captured = capsys.readouterr()
        assert "2" in captured.out

    def test_should_print_back_option_when_called(self, capsys):
        show_sample_menu()
        captured = capsys.readouterr()
        assert "0" in captured.out

    def test_should_include_menu_label_when_called(self, capsys):
        show_sample_menu()
        captured = capsys.readouterr()
        assert "시료" in captured.out


class TestShowSampleList:
    def test_should_print_empty_message_when_given_empty_list(self, capsys):
        show_sample_list([])
        captured = capsys.readouterr()
        assert captured.out.strip() != ""  # Must print something (not silent)
        assert any(word in captured.out for word in ["없", "empty", "Empty", "0건", "없습니다"])

    def test_should_print_sample_id_when_given_one_sample(self, capsys):
        sample = Sample(sample_id="S001", name="시료A", avg_production_time=2.5, yield_rate=0.95)
        show_sample_list([sample])
        captured = capsys.readouterr()
        assert "S001" in captured.out

    def test_should_print_sample_name_when_given_one_sample(self, capsys):
        sample = Sample(sample_id="S001", name="시료A", avg_production_time=2.5, yield_rate=0.95)
        show_sample_list([sample])
        captured = capsys.readouterr()
        assert "시료A" in captured.out

    def test_should_print_all_samples_when_given_multiple_samples(self, capsys):
        samples = [
            Sample(sample_id="S001", name="시료A", avg_production_time=2.5, yield_rate=0.95),
            Sample(sample_id="S002", name="시료B", avg_production_time=3.0, yield_rate=0.90),
        ]
        show_sample_list(samples)
        captured = capsys.readouterr()
        assert "S001" in captured.out
        assert "S002" in captured.out
        assert "시료A" in captured.out
        assert "시료B" in captured.out


class TestShowSampleDetail:
    def test_should_print_sample_id_when_given_sample(self, capsys):
        sample = Sample(sample_id="S001", name="시료A", avg_production_time=2.5, yield_rate=0.95)
        show_sample_detail(sample)
        captured = capsys.readouterr()
        assert "S001" in captured.out

    def test_should_print_sample_name_when_given_sample(self, capsys):
        sample = Sample(sample_id="S001", name="시료A", avg_production_time=2.5, yield_rate=0.95)
        show_sample_detail(sample)
        captured = capsys.readouterr()
        assert "시료A" in captured.out

    def test_should_print_avg_production_time_when_given_sample(self, capsys):
        sample = Sample(sample_id="S001", name="시료A", avg_production_time=2.5, yield_rate=0.95)
        show_sample_detail(sample)
        captured = capsys.readouterr()
        assert "2.5" in captured.out

    def test_should_print_yield_rate_when_given_sample(self, capsys):
        sample = Sample(sample_id="S001", name="시료A", avg_production_time=2.5, yield_rate=0.95)
        show_sample_detail(sample)
        captured = capsys.readouterr()
        assert "0.95" in captured.out
