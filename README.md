# ConsoleMVC — PoC

> **SampleOrderSystem** 프로젝트의 PoC 모듈 — 콘솔 기반 MVC 패턴 구조와 역할 분리 검증

## 개요

가상의 반도체 회사 "S-Semi"의 **시료 생산주문관리 시스템(SampleOrderSystem)** 을 개발하기 위한 4개 PoC 모듈 중 하나입니다.

이 레포는 콘솔 환경에서 **MVC(Model-View-Controller) 패턴**이 유효하게 동작하는지를 TDD 방식으로 검증합니다.  
비즈니스 로직 상세 구현은 `SampleOrderSystem` 통합 단계에서 진행하며, 여기서는 **패키지 구조와 레이어 역할 분리**에 집중합니다.

## PoC 위치

| 모듈 | 역할 |
|------|------|
| **ConsoleMVC** ← 현재 레포 | 콘솔 기반 MVC 패턴 구현 검증 |
| DataPersistence | 데이터 저장/불러오기 처리 검증 |
| DataMonitor | 데이터 모니터링/조회 검증 |
| DummyDataGenerator | 테스트용 더미 데이터 생성 검증 |

## MVC 레이어 역할

```
┌─────────────────────────────────────────────────────┐
│  사용자 입력 (콘솔)                                   │
└───────────────────┬─────────────────────────────────┘
                    │
         ┌──────────▼──────────┐
         │    Controller       │  입력 수신 → Model 조회 → View 호출
         │  (라우팅 / 조율)     │  비즈니스 로직 없음
         └──────┬──────┬───────┘
                │      │
     ┌──────────▼─┐  ┌─▼──────────┐
     │   Model    │  │    View    │
     │ (데이터)   │  │  (출력)    │
     │ 속성 정의만 │  │ print()만  │
     │ 로직 없음   │  │ input() X  │
     └────────────┘  └────────────┘
```

| 레이어 | 해야 할 것 | 하지 말아야 할 것 |
|--------|-----------|-----------------|
| **Model** | 데이터 속성 정의, enum | 콘솔 출력, 입력 처리, 계산 |
| **View** | 데이터 받아 콘솔 출력 | 비즈니스 로직, 상태 변경, input() |
| **Controller** | 입력 수신, Model/View 연결 | 직접 print(), 비즈니스 로직 |

## 디렉터리 구조

```
ConsoleMVC-YoonChangheum-22094435/
├── app/
│   ├── models/
│   │   ├── sample.py           # Sample 데이터 클래스
│   │   ├── order.py            # OrderStatus enum + Order 데이터 클래스
│   │   ├── inventory.py        # Inventory 데이터 클래스
│   │   └── production_queue.py # ProductionJob + ProductionQueue (FIFO)
│   ├── views/
│   │   ├── base_view.py        # 공통 출력 헬퍼 (header, separator, error, success)
│   │   ├── main_menu_view.py   # 메인 메뉴 출력
│   │   ├── sample_view.py      # 시료 관리 화면
│   │   ├── order_view.py       # 주문 화면
│   │   ├── monitoring_view.py  # 모니터링 화면
│   │   ├── production_view.py  # 생산 라인 화면
│   │   └── release_view.py     # 출고 처리 화면
│   ├── controllers/
│   │   ├── sample_controller.py
│   │   ├── order_controller.py
│   │   ├── monitoring_controller.py
│   │   ├── production_controller.py
│   │   └── release_controller.py
│   └── main.py                 # 진입점 — 메인 메뉴 루프
├── tests/
│   ├── conftest.py
│   ├── test_models/            # 모델 단위 테스트 (48개)
│   ├── test_views/             # 뷰 출력 단위 테스트 (71개)
│   └── test_controllers/       # 컨트롤러 단위 테스트 (74개)
├── PRD.md                      # 요구사항 및 개발 계획
├── CLAUDE.md                   # Claude Code 작업 가이드
└── requirements.txt
```

## 도메인 모델

### 주문 상태 흐름

```
RESERVED ──(승인, 재고 충분)──→ CONFIRMED ──→ RELEASE
         ──(승인, 재고 부족)──→ PRODUCING ──→ CONFIRMED ──→ RELEASE
         ──(거절)────────────→ REJECTED
```

> `REJECTED`는 모니터링에서 제외됩니다.

### 시료 (Sample)

| 필드 | 타입 | 설명 |
|------|------|------|
| `sample_id` | str | 고유 식별자 |
| `name` | str | 시료 이름 |
| `avg_production_time` | float | 평균 생산 시간 (시간/개) |
| `yield_rate` | float | 수율 (정상품 / 전체 생산량, 예: 0.9) |

### 메인 메뉴

```
1. 시료 관리       — 등록 / 목록 / 검색
2. 주문            — 접수 / 승인 / 거절
3. 모니터링        — 상태별 주문 수 + 재고 현황
4. 생산 라인       — 생산 큐 확인
5. 출고 처리       — CONFIRMED 주문 출고 실행
0. 종료
```

## 시작하기

### 요구사항

- Python 3.10+

### 설치

```bash
pip install -r requirements.txt
```

### 실행

```bash
python -m app.main
```

### 테스트

```bash
# 전체 테스트
pytest

# 레이어별 실행
pytest tests/test_models/ -v
pytest tests/test_views/ -v
pytest tests/test_controllers/ -v

# 단일 테스트
pytest tests/test_models/test_order.py::TestOrderStatus::test_should_have_exactly_five_statuses

# 커버리지 포함
pytest --cov=app
```

## 개발 방식 (TDD)

각 레이어를 **Red → Green → Refactor** 사이클로 구현했습니다.

```
[RED]    실패하는 테스트 먼저 작성
    ↓
[GREEN]  테스트를 통과하는 최소 구현
    ↓
[REFACTOR] 동작을 유지하면서 코드 정리
```

테스트 네이밍 컨벤션: `test_should_[예상동작]_when_[조건]`

```python
# 예시
def test_should_exclude_rejected_orders_when_given_mixed_orders(capsys):
    ...
```

Controller 테스트는 View를 `MagicMock`으로 대체해 레이어 간 결합을 차단합니다.

```python
def test_should_call_show_sample_list_when_list_samples_called():
    mock_view = MagicMock()
    controller = SampleController(sample_store=[sample], view=mock_view)
    controller.list_samples()
    mock_view.show_sample_list.assert_called_once_with([sample])
```

## 테스트 현황

| 레이어 | 파일 수 | 테스트 수 |
|--------|---------|----------|
| Models | 4 | 48 |
| Views | 7 | 71 |
| Controllers | 5 | 74 |
| **합계** | **16** | **193** |

## Git 태그

| 태그 | 내용 |
|------|------|
| `phase0-setup` | 프로젝트 초기 설정 및 스캐폴딩 |
| `phase1-models` | Model 스켈레톤 TDD 완성 |
| `phase2-views` | View 스켈레톤 TDD 완성 |
| `phase3-controllers` | Controller 스켈레톤 TDD 완성 |
| `phase4-integration` | 통합 완성 및 코드 품질 검증 |
