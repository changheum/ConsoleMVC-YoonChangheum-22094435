"""
Tests for ProductionJob dataclass and ProductionQueue FIFO container.
RED phase: all tests written before any production code exists.
"""
import pytest
from app.models.production_queue import ProductionJob, ProductionQueue


class TestProductionJobCreation:
    def test_should_store_order_id_when_created(self):
        # Arrange / Act
        job = ProductionJob(
            order_id="O-001",
            sample_id="S-001",
            required_quantity=50,
        )
        # Assert
        assert job.order_id == "O-001"

    def test_should_store_sample_id_when_created(self):
        job = ProductionJob(
            order_id="O-001",
            sample_id="S-001",
            required_quantity=50,
        )
        assert job.sample_id == "S-001"

    def test_should_store_required_quantity_when_created(self):
        job = ProductionJob(
            order_id="O-002",
            sample_id="S-003",
            required_quantity=30,
        )
        assert job.required_quantity == 30

    def test_should_be_equal_when_all_fields_are_identical(self):
        job_a = ProductionJob(order_id="O-001", sample_id="S-001", required_quantity=10)
        job_b = ProductionJob(order_id="O-001", sample_id="S-001", required_quantity=10)
        assert job_a == job_b

    def test_should_not_be_equal_when_order_id_differs(self):
        job_a = ProductionJob(order_id="O-001", sample_id="S-001", required_quantity=10)
        job_b = ProductionJob(order_id="O-002", sample_id="S-001", required_quantity=10)
        assert job_a != job_b


class TestProductionQueueEmpty:
    def test_should_be_empty_when_newly_created(self):
        # Arrange / Act
        queue = ProductionQueue()
        # Assert
        assert queue.is_empty() is True

    def test_should_have_size_zero_when_newly_created(self):
        queue = ProductionQueue()
        assert queue.size() == 0


class TestProductionQueueEnqueue:
    def test_should_not_be_empty_when_one_job_enqueued(self):
        # Arrange
        queue = ProductionQueue()
        job = ProductionJob(order_id="O-001", sample_id="S-001", required_quantity=5)
        # Act
        queue.enqueue(job)
        # Assert
        assert queue.is_empty() is False

    def test_should_have_size_one_when_one_job_enqueued(self):
        queue = ProductionQueue()
        job = ProductionJob(order_id="O-001", sample_id="S-001", required_quantity=5)
        queue.enqueue(job)
        assert queue.size() == 1

    def test_should_increment_size_when_multiple_jobs_enqueued(self):
        queue = ProductionQueue()
        job_a = ProductionJob(order_id="O-001", sample_id="S-001", required_quantity=5)
        job_b = ProductionJob(order_id="O-002", sample_id="S-002", required_quantity=3)
        queue.enqueue(job_a)
        queue.enqueue(job_b)
        assert queue.size() == 2


class TestProductionQueuePeek:
    def test_should_return_first_job_when_peeked(self):
        # Arrange
        queue = ProductionQueue()
        job_first = ProductionJob(order_id="O-001", sample_id="S-001", required_quantity=5)
        job_second = ProductionJob(order_id="O-002", sample_id="S-002", required_quantity=3)
        queue.enqueue(job_first)
        queue.enqueue(job_second)
        # Act
        result = queue.peek()
        # Assert
        assert result == job_first

    def test_should_not_remove_job_when_peeked(self):
        queue = ProductionQueue()
        job = ProductionJob(order_id="O-001", sample_id="S-001", required_quantity=5)
        queue.enqueue(job)
        queue.peek()
        assert queue.size() == 1

    def test_should_return_none_when_peeked_on_empty_queue(self):
        queue = ProductionQueue()
        assert queue.peek() is None


class TestProductionQueueDequeue:
    def test_should_return_first_enqueued_job_when_dequeued(self):
        # Arrange
        queue = ProductionQueue()
        job_first = ProductionJob(order_id="O-001", sample_id="S-001", required_quantity=5)
        job_second = ProductionJob(order_id="O-002", sample_id="S-002", required_quantity=3)
        queue.enqueue(job_first)
        queue.enqueue(job_second)
        # Act
        result = queue.dequeue()
        # Assert — FIFO: first in, first out
        assert result == job_first

    def test_should_return_second_job_when_dequeued_twice(self):
        queue = ProductionQueue()
        job_first = ProductionJob(order_id="O-001", sample_id="S-001", required_quantity=5)
        job_second = ProductionJob(order_id="O-002", sample_id="S-002", required_quantity=3)
        queue.enqueue(job_first)
        queue.enqueue(job_second)
        queue.dequeue()
        result = queue.dequeue()
        assert result == job_second

    def test_should_decrement_size_when_dequeued(self):
        queue = ProductionQueue()
        job = ProductionJob(order_id="O-001", sample_id="S-001", required_quantity=5)
        queue.enqueue(job)
        queue.dequeue()
        assert queue.size() == 0

    def test_should_be_empty_when_all_jobs_dequeued(self):
        queue = ProductionQueue()
        job = ProductionJob(order_id="O-001", sample_id="S-001", required_quantity=5)
        queue.enqueue(job)
        queue.dequeue()
        assert queue.is_empty() is True

    def test_should_return_none_when_dequeued_from_empty_queue(self):
        queue = ProductionQueue()
        assert queue.dequeue() is None

    def test_should_maintain_fifo_order_when_three_jobs_enqueued(self):
        # Arrange
        queue = ProductionQueue()
        jobs = [
            ProductionJob(order_id=f"O-00{i}", sample_id="S-001", required_quantity=i)
            for i in range(1, 4)
        ]
        for job in jobs:
            queue.enqueue(job)
        # Act / Assert — dequeue order must match enqueue order
        for expected_job in jobs:
            assert queue.dequeue() == expected_job
