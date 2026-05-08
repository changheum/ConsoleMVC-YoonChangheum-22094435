"""
Tests for OrderStatus enum and Order model.
RED phase: all tests written before any production code exists.
"""
import pytest
from app.models.order import Order, OrderStatus


class TestOrderStatus:
    def test_should_have_reserved_status(self):
        # Assert
        assert OrderStatus.RESERVED is not None

    def test_should_have_rejected_status(self):
        assert OrderStatus.REJECTED is not None

    def test_should_have_producing_status(self):
        assert OrderStatus.PRODUCING is not None

    def test_should_have_confirmed_status(self):
        assert OrderStatus.CONFIRMED is not None

    def test_should_have_release_status(self):
        assert OrderStatus.RELEASE is not None

    def test_should_have_exactly_five_statuses(self):
        assert len(OrderStatus) == 5

    def test_should_be_distinguishable_from_each_other(self):
        statuses = list(OrderStatus)
        # All values must be unique
        assert len(set(statuses)) == len(statuses)


class TestOrderCreation:
    def test_should_store_order_id_when_created(self):
        # Arrange / Act
        order = Order(
            order_id="O-001",
            sample_id="S-001",
            customer_name="Seoul Fab",
            quantity=10,
            status=OrderStatus.RESERVED,
        )
        # Assert
        assert order.order_id == "O-001"

    def test_should_store_sample_id_when_created(self):
        order = Order(
            order_id="O-001",
            sample_id="S-001",
            customer_name="Seoul Fab",
            quantity=10,
            status=OrderStatus.RESERVED,
        )
        assert order.sample_id == "S-001"

    def test_should_store_customer_name_when_created(self):
        order = Order(
            order_id="O-002",
            sample_id="S-002",
            customer_name="Daejeon Lab",
            quantity=5,
            status=OrderStatus.RESERVED,
        )
        assert order.customer_name == "Daejeon Lab"

    def test_should_store_quantity_when_created(self):
        order = Order(
            order_id="O-003",
            sample_id="S-001",
            customer_name="Busan Uni",
            quantity=20,
            status=OrderStatus.RESERVED,
        )
        assert order.quantity == 20

    def test_should_store_status_when_created(self):
        order = Order(
            order_id="O-004",
            sample_id="S-001",
            customer_name="Client A",
            quantity=1,
            status=OrderStatus.PRODUCING,
        )
        assert order.status == OrderStatus.PRODUCING

    def test_should_default_status_to_reserved_when_not_specified(self):
        order = Order(
            order_id="O-005",
            sample_id="S-001",
            customer_name="Client B",
            quantity=3,
        )
        assert order.status == OrderStatus.RESERVED

    def test_should_be_equal_when_all_fields_are_identical(self):
        order_a = Order(
            order_id="O-010",
            sample_id="S-001",
            customer_name="Test Co",
            quantity=5,
            status=OrderStatus.CONFIRMED,
        )
        order_b = Order(
            order_id="O-010",
            sample_id="S-001",
            customer_name="Test Co",
            quantity=5,
            status=OrderStatus.CONFIRMED,
        )
        assert order_a == order_b

    def test_should_not_be_equal_when_order_id_differs(self):
        order_a = Order(
            order_id="O-001",
            sample_id="S-001",
            customer_name="Test Co",
            quantity=5,
            status=OrderStatus.RESERVED,
        )
        order_b = Order(
            order_id="O-002",
            sample_id="S-001",
            customer_name="Test Co",
            quantity=5,
            status=OrderStatus.RESERVED,
        )
        assert order_a != order_b

    def test_should_allow_status_assigned_to_any_valid_enum_value(self):
        for status in OrderStatus:
            order = Order(
                order_id="O-100",
                sample_id="S-001",
                customer_name="Any",
                quantity=1,
                status=status,
            )
            assert order.status == status
