from app.models.inventory import Inventory
from app.models.production_queue import ProductionQueue
from app.controllers.sample_controller import SampleController
from app.controllers.order_controller import OrderController
from app.controllers.monitoring_controller import MonitoringController
from app.controllers.production_controller import ProductionController
from app.controllers.release_controller import ReleaseController
import app.views.main_menu_view as main_menu_view
import app.views.sample_view as sample_view
import app.views.order_view as order_view
import app.views.monitoring_view as monitoring_view
import app.views.production_view as production_view
import app.views.release_view as release_view
from app.views.base_view import print_header, print_error


def main():
    sample_store = []
    order_store = []
    inventory_store = []
    production_queue = ProductionQueue()

    sample_ctrl = SampleController(sample_store=sample_store, view=sample_view)
    order_ctrl = OrderController(order_store=order_store, view=order_view)
    monitoring_ctrl = MonitoringController(
        order_store=order_store,
        inventory_store=inventory_store,
        view=monitoring_view,
    )
    production_ctrl = ProductionController(production_queue=production_queue, view=production_view)
    release_ctrl = ReleaseController(order_store=order_store, view=release_view)

    while True:
        print_header("S-Semi 시료 생산주문관리 시스템")
        main_menu_view.show_main_menu()
        choice = input("선택: ").strip()

        if choice == "1":
            sample_ctrl.run()
        elif choice == "2":
            order_ctrl.run()
        elif choice == "3":
            monitoring_ctrl.run()
        elif choice == "4":
            production_ctrl.run()
        elif choice == "5":
            release_ctrl.run()
        elif choice == "0":
            print("시스템을 종료합니다.")
            break
        else:
            print_error("올바른 메뉴를 선택하세요.")


if __name__ == "__main__":
    main()
