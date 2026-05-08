"""
Tests for the Sample model.
RED phase: all tests written before any production code exists.
"""
import pytest
from app.models.sample import Sample


class TestSampleCreation:
    def test_should_store_sample_id_when_created(self):
        # Arrange / Act
        sample = Sample(
            sample_id="S-001",
            name="GaN Wafer",
            avg_production_time=2.5,
            yield_rate=0.9,
        )
        # Assert
        assert sample.sample_id == "S-001"

    def test_should_store_name_when_created(self):
        # Arrange / Act
        sample = Sample(
            sample_id="S-001",
            name="GaN Wafer",
            avg_production_time=2.5,
            yield_rate=0.9,
        )
        # Assert
        assert sample.name == "GaN Wafer"

    def test_should_store_avg_production_time_when_created(self):
        # Arrange / Act
        sample = Sample(
            sample_id="S-002",
            name="Si Wafer",
            avg_production_time=1.5,
            yield_rate=0.85,
        )
        # Assert
        assert sample.avg_production_time == 1.5

    def test_should_store_yield_rate_when_created(self):
        # Arrange / Act
        sample = Sample(
            sample_id="S-002",
            name="Si Wafer",
            avg_production_time=1.5,
            yield_rate=0.85,
        )
        # Assert
        assert sample.yield_rate == 0.85

    def test_should_be_equal_when_all_fields_are_identical(self):
        # Arrange
        sample_a = Sample(
            sample_id="S-003",
            name="SiC",
            avg_production_time=3.0,
            yield_rate=0.75,
        )
        sample_b = Sample(
            sample_id="S-003",
            name="SiC",
            avg_production_time=3.0,
            yield_rate=0.75,
        )
        # Act / Assert
        assert sample_a == sample_b

    def test_should_not_be_equal_when_sample_id_differs(self):
        # Arrange
        sample_a = Sample(
            sample_id="S-001",
            name="GaN Wafer",
            avg_production_time=2.5,
            yield_rate=0.9,
        )
        sample_b = Sample(
            sample_id="S-002",
            name="GaN Wafer",
            avg_production_time=2.5,
            yield_rate=0.9,
        )
        # Act / Assert
        assert sample_a != sample_b

    def test_should_accept_float_avg_production_time_when_given_integer(self):
        # Arrange / Act — integers must be accepted and stored as float
        sample = Sample(
            sample_id="S-010",
            name="Test",
            avg_production_time=3,
            yield_rate=1.0,
        )
        # Assert
        assert sample.avg_production_time == 3
