# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is the **ConsoleMVC** PoC module for the `SampleOrderSystem` — a semiconductor sample production order management system (반도체 시료 생산주문관리 시스템) for the fictional company "S-Semi". The goal is to validate a console-based MVC pattern before integration into the full system.

## Commands

```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_models/test_order.py

# Run a single test by name
pytest tests/test_models/test_order.py::test_should_transition_to_confirmed_when_stock_sufficient

# Run tests with verbose output
pytest -v

# Run tests and show coverage
pytest --cov=app
```

## Planned MVC Architecture

```
app/
├── models/
│   ├── sample.py           # Sample entity: id, name, avg_production_time, yield_rate
│   ├── order.py            # Order entity + OrderStatus enum (state machine)
│   ├── inventory.py        # Per-sample stock tracking + status thresholds
│   └── production_queue.py # FIFO queue for production jobs
├── views/
│   ├── base_view.py        # Shared console output helpers
│   ├── main_menu_view.py
│   ├── sample_view.py
│   ├── order_view.py
│   ├── monitoring_view.py
│   ├── production_view.py
│   └── release_view.py
├── controllers/
│   ├── sample_controller.py
│   ├── order_controller.py
│   ├── monitoring_controller.py
│   ├── production_controller.py
│   └── release_controller.py
└── main.py                 # Entry point: main menu loop
tests/
├── conftest.py             # Shared fixtures
├── test_models/
├── test_controllers/
└── test_views/
```

## Domain Model (from PRD)

### Order State Machine
```
RESERVED ──(approve, stock OK)──→ CONFIRMED ──→ RELEASE
         ──(approve, stock low)──→ PRODUCING ──→ CONFIRMED ──→ RELEASE
         ──(reject)─────────────→ REJECTED
```
- `REJECTED` is excluded from all monitoring views.

### Sample Attributes
| Field | Type | Description |
|---|---|---|
| `sample_id` | str | Unique identifier |
| `name` | str | Display name |
| `avg_production_time` | float | Hours per unit |
| `yield_rate` | float | Good units / total units (e.g. 0.9) |

### Key Business Formulas
```python
# When stock is insufficient, calculate production order:
actual_qty = ceil(shortage / (yield_rate * 0.9))
total_production_time = avg_production_time * actual_qty
```

### Inventory Status Thresholds
- **여유 (OK)**: stock ≥ pending order quantity
- **부족 (Low)**: stock < pending order quantity but > 0
- **고갈 (Empty)**: stock == 0

## TDD Conventions

- Test names follow: `test_should_[expected_behavior]_when_[condition]`
- Each test covers exactly one behavior (AAA: Arrange-Act-Assert)
- Controllers receive dependencies via constructor injection — use mocks/fakes in tests
- Views receive data objects — test output strings, not side effects on `sys.stdout` directly

## Available Agents

| Agent | Trigger |
|---|---|
| `tdd-ocp-implementer` | Implementing features from PRD using TDD + OCP |
| `planning-consistency-validator` | Cross-document consistency check |
| `code-quality-validator` | After implementing a unit of code |
| `prd-compliance-reviewer` | Verify implementation matches PRD requirements |
