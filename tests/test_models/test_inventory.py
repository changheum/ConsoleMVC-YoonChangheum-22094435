"""
Tests for the Inventory model.
RED phase: all tests written before any production code exists.
"""
import pytest
from app.models.inventory import Inventory


class TestInventoryCreation:
    def test_should_store_sample_id_when_created(self):
        # Arrange / Act
        inventory = Inventory(sample_id="S-001", quantity=100)
        # Assert
        assert inventory.sample_id == "S-001"

    def test_should_store_quantity_when_created(self):
        # Arrange / Act
        inventory = Inventory(sample_id="S-001", quantity=100)
        # Assert
        assert inventory.quantity == 100

    def test_should_store_zero_quantity_when_given_zero(self):
        inventory = Inventory(sample_id="S-002", quantity=0)
        assert inventory.quantity == 0

    def test_should_be_equal_when_all_fields_are_identical(self):
        # Arrange
        inv_a = Inventory(sample_id="S-001", quantity=50)
        inv_b = Inventory(sample_id="S-001", quantity=50)
        # Act / Assert
        assert inv_a == inv_b

    def test_should_not_be_equal_when_sample_id_differs(self):
        inv_a = Inventory(sample_id="S-001", quantity=50)
        inv_b = Inventory(sample_id="S-002", quantity=50)
        assert inv_a != inv_b

    def test_should_not_be_equal_when_quantity_differs(self):
        inv_a = Inventory(sample_id="S-001", quantity=10)
        inv_b = Inventory(sample_id="S-001", quantity=20)
        assert inv_a != inv_b
