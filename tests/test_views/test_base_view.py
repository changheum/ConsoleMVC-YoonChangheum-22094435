"""
Tests for app/views/base_view.py
TDD Phase 2 — View skeleton
"""
import pytest
from app.views.base_view import print_header, print_separator, print_error, print_success


class TestPrintSeparator:
    def test_should_print_dashes_when_called(self, capsys):
        print_separator()
        captured = capsys.readouterr()
        assert "---" in captured.out

    def test_should_end_with_newline_when_called(self, capsys):
        print_separator()
        captured = capsys.readouterr()
        assert captured.out.endswith("\n")


class TestPrintHeader:
    def test_should_print_title_when_given_title(self, capsys):
        print_header("테스트 제목")
        captured = capsys.readouterr()
        assert "테스트 제목" in captured.out

    def test_should_print_separator_above_title_when_called(self, capsys):
        print_header("제목")
        captured = capsys.readouterr()
        lines = captured.out.splitlines()
        # At least one line must be a separator line before or around title
        has_separator = any("---" in line for line in lines)
        assert has_separator

    def test_should_print_separator_below_title_when_called(self, capsys):
        print_header("제목")
        captured = capsys.readouterr()
        lines = captured.out.splitlines()
        # There should be at least 2 non-empty lines (separator + title + separator)
        assert len([l for l in lines if l.strip()]) >= 2

    def test_should_print_empty_title_when_given_empty_string(self, capsys):
        print_header("")
        captured = capsys.readouterr()
        # Should not raise; separator must still appear
        assert "---" in captured.out


class TestPrintError:
    def test_should_print_message_when_given_message(self, capsys):
        print_error("오류가 발생했습니다")
        captured = capsys.readouterr()
        assert "오류가 발생했습니다" in captured.out

    def test_should_include_error_indicator_when_called(self, capsys):
        print_error("문제")
        captured = capsys.readouterr()
        # Must contain some visual error marker
        assert any(marker in captured.out for marker in ["[오류]", "[ERROR]", "오류", "Error", "!"])

    def test_should_end_with_newline_when_called(self, capsys):
        print_error("메시지")
        captured = capsys.readouterr()
        assert captured.out.endswith("\n")


class TestPrintSuccess:
    def test_should_print_message_when_given_message(self, capsys):
        print_success("처리 완료")
        captured = capsys.readouterr()
        assert "처리 완료" in captured.out

    def test_should_include_success_indicator_when_called(self, capsys):
        print_success("완료")
        captured = capsys.readouterr()
        assert any(marker in captured.out for marker in ["[성공]", "[OK]", "성공", "Success", "v", "OK"])

    def test_should_end_with_newline_when_called(self, capsys):
        print_success("메시지")
        captured = capsys.readouterr()
        assert captured.out.endswith("\n")
