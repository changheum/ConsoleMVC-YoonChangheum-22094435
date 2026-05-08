# 배경
여기 가상의 반도체 회사 "S-Semi" 가 있습니다.
이 회사는 다양한 종류의 반도체 시료(Sample)를 생산하여 연구소, 팹리스(Fabless) 업체, 대학 연구실 등의 고객에게
납품하고 있습니다.
시료는 주문이 들어오면 웨이퍼 공정 설비를 통해 제작되고, 검수를 거쳐 고객에게 출고됩니다.
그런데 최근 들어 주문량이 급증하면서 문제가 생겼습니다.
"어, 이 주문 처리됐나요?"
"공정 예약을 했는데, 언제 완성되는지 모르겠어요."
"이미 충분한 시료 재고가 있는데, 왜 추가 공정이 돌아가고 있나요?“
엑셀과 메모장으로 주문을 관리하다 보니, 실수가 잦고 재고와 공정 현황을 한눈에 파악하기 어려웠습니다.
이러한 이유로 S-Semi에서는 더 체계적인 시료 관리를 위한 "반도체 시료 생산주문관리 시스템" 을 개발하기로 결정
했습니다.

# 흐름
시료에 대한 주문 등록을 하면 주문을 Reserved 상태로 등록함
Reserved에 대해 승인/거절을 입력 할 수 있음
거절 되면 주문을 Rejected 상태로 변경
주문이 승인 되면 재고 확인 과정을 거침
시료 재고확인 후, 주문에 대해 충분한 재고가 있으면 시료를 사용해서 주문을 출고하고 주문을  CONFIRMED(출고준비) 상태로 바꿈
출고준비상태의 주문을 RELEASED(출고 처리) 상태로 바꾸면 시료를 사용해서 주문을 출고시키고 정보를 완료 정보를 저장
재고확인 과정에서 재고가 부족하면 부족분량을 생산 요청하여 주문이 PRODUCING 상태가 됨.
부족분의 시료가 생산 완료가 되면 시료를 사용해서 주문을 CONFIRMED(출고준비) 상태로 바꿈(생산에 걸리는 시간은 수율과 생산시간을 고려해야한다)

# 모든 주문은 아래의 상태를 보유
REJECTED는 거절된 주문으로 정상 흐름 외의 상태이며 모니터링에서 제외

RESERVED / 주문 접수
REJECTED / 주문 거절
PRODUCING / 주문 승인 완료 및 재고 부족으로 생산 중
CONFIRMED / 주문 승인 완료 및 출고 대기 중
RELEASE / 출고 완료

# 용어 및 정의
## 시료 
시료(Sample)는 이 시스템의 가장 기본이 되는 단위
각 시료는 고유한 이름과 속성을 가지며, 시스템에 등록된 시료만 주문 가능

# 메인 메뉴 
전체 시료에 대한 요약 정보를 확인할 수 있게 한다.
기능(메뉴)별 선택 화면을 Display 해서 선택할 수 있게 한다.

## 메인 메뉴 항목과 의미
1. 시료 관리 : 새로운 시료 등록, 목록 조회, 이름 검색 기능
2. 주문 (접수 / 승인 / 거절) :  생산 라인 담당자의 승인·거절 처리
3. 모니터링 : 상태별 주문 수 및 시료별 재고 현황 확인
4. 생산 라인 : 현재 생산 중인 시료 및 대기 중인 생산 큐 확인
5. 출고 처리 : CONFIRMED 상태 주문에 대해 출고 실행
0. 종료

### 시료 관리 메뉴
1. 시료 등록 : 새로운 시료를 시스템에 추가(속성 값 : 시료 ID, 이름, 평균 생산시간, 수율)
2. 시료 조회 : 등록된 모든 시료 목록을 확인(현재 재고 수량도 함께 표시)
3. 시료 검색 : 이름 등 속성으로 특정 시료를 검색
0. 뒤로가기
* 수율이란? : (정상적인 시료 / 총 생산 시료)
ex) 100개 생산 중 정상적인 물품 90개 = 0.9

### 주문 (접수 / 승인 / 거절) 메뉴
1. 접수
고객이 시료를 요청하면 주문 담당자가 주문을 생성 가능
시료 예약
- 시료 목록을 보고 고객이 원하는 시료와 수량을 주문
- 접수되면 주문 상태는 RESERVED
예약시 입력 값
- 시료 ID
- 고객명
- 주문 수량

2. 승인/거절
접수된 주문(RESERVED) 목록을 확인. 특정 주문에 대하여 승인 혹은 거절 할 수 있는 화면
RESERVED 상태의 주문 목록 Display하여 확인 가능하게 함 

a) 주문 승인
접수된 특정 주문에 대해 승인
- 승인시 재고 상황에 따라 2가지 방식으로 자동으로 처리
- 재고가 충분한 경우 → 시료를 사용하고, 주문을 즉시 CONFIRMED 상태로 전환
- 재고가 부족한 경우 → 모자란 시료 분량을 생산 라인에 자동으로 등록, 주문 상태를 PRODUCING으로 전환
b) 주문 거절
접수된 특정 주문에 대해 거절
즉시 REJECTED 상태로 전환

### 모니터링 메뉴
담당자가 현재 시스템의 상태를 한눈에 파악할 수 있도록 구성

주문량 확인
- 현재 상태별(RESERVED/CONFIRMED/ PRODUCING / RELEASE) 목록을 확인
- REJECTED 는 유효한 주문이 아니므로 보여주지 않음

재고량 확인
각 시료별 현재 재고 수량을 확인
주문대비 재고 수량에 따라 상태도 표기
- 여유 : 주문대비 재고 충분 상태
- 부족 : 주문대비 재고 수량 부족 상태
- 고갈 : 수량이 0인 상태

### 생산 라인 메뉴
생산라인에 대한 정보를 Display
주문량에 대한 부족분을 생산하되, 수율 및 오차를 고려하여 시료를 생산
- 실 생산량 : ceil(부족분 / (수율 * 0.9))
- 총 생산 시간 : 평균 생산시간 * 실 생산량
- 생산 완료시 주문상태 PRODUCING -> CONFIRMED 변경

생산 현황 표기
- 현재 생산중인 시료에 대한 정보 표기
  ex) 주문 정보, 현재까지의 생산량 등
대기 주문 표기
생산라인의 대기열인 생산 큐를 이용
생산 작업을 대기하고 있는 목록을 출력
- 스케쥴링 전략 : FIFO

### 출고 처리 메뉴
재고가 충분해진 CONFIRMED 주문에 대하여 출고를 처리할 수 있는 화면
특정 주문에 대해 출고를 실행
주문 상태가 RELEASE로 전환

---

# 개발 계획 (ConsoleMVC PoC)

> **PoC 범위**: MVC 스켈레톤 코드 — Model / Controller / View 패키지 구조와 역할 분리 완성
> 비즈니스 로직 상세 구현은 `SampleOrderSystem` 통합 단계에서 진행한다.
>
> 각 Phase는 TDD(Red→Green→Refactor) 사이클로 구현하며, 완료 후 승인을 받아 Git push 한다.
> 사용 Agent: `tdd-ocp-implementer` (구현), `code-quality-validator` (품질)

## Phase 0: 프로젝트 설정 ✅
- [x] CLAUDE.md 작성 (아키텍처, 명령어, 도메인 문서화)
- [x] PRD.md 개발 계획 섹션 추가
- [x] 디렉터리 스캐폴딩 (`app/`, `tests/`, `requirements.txt`, `conftest.py`)
- [x] `.gitignore` 추가
- **완료 기준**: pytest 실행 가능한 빈 프로젝트 구조 ✅

## Phase 1: Model 스켈레톤 TDD
> 역할: 도메인 데이터 구조 정의. 비즈니스 로직 없이 속성과 상태 표현에 집중.

- [x] `app/models/sample.py` — Sample 데이터 클래스 (sample_id, name, avg_production_time, yield_rate)
- [x] `app/models/order.py` — OrderStatus enum + Order 데이터 클래스
- [x] `app/models/inventory.py` — Inventory 데이터 클래스 (sample_id, quantity)
- [x] `app/models/production_queue.py` — ProductionJob 데이터 클래스 + ProductionQueue (FIFO 컨테이너)
- [x] `tests/test_models/` — 각 모델 생성/속성 접근 단위 테스트 (48개 통과)
- **완료 기준**: `pytest tests/test_models/ -v` 전체 통과
- **담당 Agent**: `tdd-ocp-implementer`

## Phase 2: View 스켈레톤 TDD
> 역할: 콘솔 출력 전담. 데이터를 받아 문자열로 렌더링. 입력/로직 없음.

- [ ] `app/views/base_view.py` — 공통 출력 메서드 (구분선, 헤더 등)
- [ ] `app/views/main_menu_view.py` — 메인 메뉴 출력
- [ ] `app/views/sample_view.py` — 시료 목록/상세 출력
- [ ] `app/views/order_view.py` — 주문 목록 출력
- [ ] `app/views/monitoring_view.py` — 상태별 요약 출력
- [ ] `app/views/production_view.py` — 생산 큐 현황 출력
- [ ] `app/views/release_view.py` — 출고 대상 목록 출력
- [ ] `tests/test_views/` — 각 뷰의 출력 문자열 단위 테스트
- **완료 기준**: `pytest tests/test_views/ -v` 전체 통과
- **담당 Agent**: `tdd-ocp-implementer`

## Phase 3: Controller 스켈레톤 TDD
> 역할: 사용자 입력 처리 + Model 조회/변경 + View 호출 조율. 레이어 간 접착제.

- [ ] `app/controllers/sample_controller.py` — 시료 메뉴 라우팅
- [ ] `app/controllers/order_controller.py` — 주문 메뉴 라우팅
- [ ] `app/controllers/monitoring_controller.py` — 모니터링 메뉴 라우팅
- [ ] `app/controllers/production_controller.py` — 생산 라인 메뉴 라우팅
- [ ] `app/controllers/release_controller.py` — 출고 메뉴 라우팅
- [ ] `tests/test_controllers/` — 컨트롤러가 올바른 뷰/모델을 호출하는지 단위 테스트
- **완료 기준**: `pytest tests/test_controllers/ -v` 전체 통과
- **담당 Agent**: `tdd-ocp-implementer`, `code-quality-validator`

## Phase 4: 통합 완성
> 역할: main.py로 전체 루프 연결. MVC 역할 분리 최종 검증.

- [ ] `app/main.py` — 메인 메뉴 루프 (Controller 들을 연결)
- [ ] `pytest -v` 전체 통과 확인
- [ ] 코드 품질 최종 점검
- **완료 기준**: 모든 테스트 통과 + MVC 레이어 역할 분리 명확
- **담당 Agent**: `code-quality-validator`

## 진행 상태
| Phase | 상태 | Git Tag |
|-------|------|---------|
| Phase 0 | ✅ 완료 | `phase0-setup` |
| Phase 1 | ✅ 완료 | `phase1-models` |
| Phase 2 | ⏳ 대기 | `phase2-views` |
| Phase 3 | ⏳ 대기 | `phase3-controllers` |
| Phase 4 | ⏳ 대기 | `phase4-integration` |

