import threading
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI


# 문 열기 클래스
class OpenDoorController:
    def __init__(self, car_controller):
        self.car_controller = car_controller

    def handle_right_door_open_controller(self):
        current_right_door_status = self.car_controller.get_right_door_status()
        current_right_door_lock = self.car_controller.get_right_door_lock()
        # 오른쪽 문이 닫혀 있을 때
        if current_right_door_status == "CLOSED":
            # 오른쪽 문이 잠겨 있을 때
            if current_right_door_lock == "LOCKED":
                print("[IGNORE]문이 잠겨 있어 문 닫힘 상태 유지")
            # 오른쪽 문이 잠겨 있지 않을 때
            elif current_right_door_lock == "OPEN":
                print("문 열림")
                self.car_controller.open_right_door()
        # 오른쪽 문이 열려 있을 때 오른쪽 문 열기 명령을 무시
        elif current_right_door_status == "OPEN":
            print("[IGNORE]문이 이미 열려 있음")

    def handle_left_door_open_controller(self):
        current_left_door_status = self.car_controller.get_left_door_status()
        current_left_door_lock = self.car_controller.get_left_door_lock()
        # 왼쪽 문이 닫혀 있을 때
        if current_left_door_status == "CLOSED":
            # 왼쪽 문이 잠겨 있을 때
            if current_left_door_lock == "LOCKED":
                print("[IGNORE]문이 잠겨 있어 문 닫힘 상태 유지")
            # 왼쪽 문이 잠겨 있지 않을 때
            elif current_left_door_lock == "OPEN":
                print("문 열림")
                self.car_controller.open_left_door()
        # 왼쪽 문이 열려 있을 때 왼쪽 문 열기 명령을 무시
        elif current_left_door_status == "OPEN":
            print("[IGNORE]문이 이미 열려 있음")
    

# 문 닫기 클래스
class ClosedDoorController:
    def __init__(self, car_controller):
        self.car_controller = car_controller
            
    def handle_right_door_closed_controller(self):
        current_right_door_status = self.car_controller.get_right_door_status()
        # 오른쪽 문이 열려 있을 때
        # 잠겨 있든 아니든 문 닫기 가능
        if current_right_door_status == "OPEN":
            print("문 닫힘")
            self.car_controller.close_right_door()
        # 오른쪽 문이 닫혀 있을 때 오른쪽 문 닫기 명령을 무시
        elif current_right_door_status == "CLOSED":
            print("[IGNORE]문이 이미 닫혀 있음")

    def handle_left_door_closed_controller(self):
        current_left_door_status = self.car_controller.get_left_door_status()
        # 왼쪽 문이 열려 있을 때
        # 잠겨 있든 아니든 문 닫기 가능
        if current_left_door_status == "OPEN":
            print("문 닫힘")
            self.car_controller.close_left_door()
        # 왼쪽 문이 닫혀 있을 때 왼쪽 문 닫기 명령을 무시
        elif current_left_door_status == "CLOSED":
            print("[IGNORE]문이 이미 닫혀 있음")


# 트렁크 제어 클래스
class TrunkController:
    def __init__(self, car_controller):
        self.car_controller = car_controller
        self.trunk_status = self.car_controller.get_trunk_status()
        self.current_speed = self.car_controller.get_speed()

    # 트렁크 열기
    def handle_trunk_open_controller(self):
        # 차가 정차 중 일때
        if self.current_speed == 0:
            # 트렁크가 닫혀 있으면(trunk_status=true)
            if self.trunk_status:
                self.car_controller.open_trunk()
                print("트렁크 열림")
            # 트렁크가 열려 있으면
            else:
                print("[IGNORE] 트렁크가 이미 열려 있음")
        # 차가 주행 중 일때
        elif self.current_speed > 0:
            print("[IGNORE]차량이 주행 중임으로 트렁크를 열 수 없음")

    # 트렁크 닫기
    def handle_trunk_closed_controller(self):
        # 트렁크가 열려 있으면(trunk_status=false)
        if not(self.trunk_status):
            self.car_controller.close_trunk()
            print("트렁크 닫힘")
        # 트렁크가 닫혀 있으면
        else:
            print("[IGNORE] 트렁크가 이미 닫혀 있음")
        #  차가 정차 중 일때
        # if self.current_speed == 0:
        #      트렁크가 열려 있으면(trunk_status=false)
        #     if not(self.trunk_status):
        #         self.car_controller.close_trunk()
        #         print("트렁크 닫힘")
        #      트렁크가 닫혀 있으면
        #     else:
        #         print("[IGNORE] 트렁크가 이미 닫혀 있음")
        #  차가 주행 중 일때
        # elif self.current_speed > 0:
        #     print("[IGNORE]차량이 주행 중임으로 트렁크를 닫을 수 없음")

class CarCommandExecutor:
    def __init__(self, car_controller):
        self.car_controller = car_controller
        self.door_open_controller = OpenDoorController(car_controller)
        self.door_closed_controller = ClosedDoorController(car_controller)
        self.trunk_controller = TrunkController(car_controller)

    def execute_command(self, command):
        if command == "ENGINE_BTN":
            car_controller.toggle_engine() # ?떆?룞 ON / OFF
        elif command == "ACCELERATE":
            car_controller.accelerate() # ?냽?룄 +10
        elif command == "BRAKE":
            car_controller.brake() # ?냽?룄 -10
        elif command == "LOCK":
            car_controller.lock_vehicle() # 李⑤웾?옞湲?
        elif command == "UNLOCK":
            car_controller.unlock_vehicle() # 李⑤웾?옞湲덊빐?젣
        elif command == "LEFT_DOOR_LOCK":
            car_controller.lock_left_door() # ?쇊履쎈Ц ?옞湲?
        elif command == "LEFT_DOOR_UNLOCK":
            car_controller.unlock_left_door() # ?쇊履쎈Ц ?옞湲덊빐?젣
        elif command == "LEFT_DOOR_OPEN":
            return self.door_open_controller.handle_left_door_open_controller() # 왼쪽문 열기
        elif command == "LEFT_DOOR_CLOSE":
            return self.door_closed_controller.handle_left_door_closed_controller() # 왼쪽문 닫기
        elif command == "right_DOOR_OPEN":
            return self.door_open_controller.handle_right_door_open_controller() # 오른쪽문 열기
        elif command == "right_DOOR_CLOSE":
            return self.door_closed_controller.handle_right_door_closed_controller() # 오른쪽문 닫기    
        elif command == "TRUNK_OPEN":
            return self.trunk_controller.handle_trunk_open_controller() # 트렁크 열기
        elif command == "TRUNK_CLOSED":
            return self.trunk_controller.handle_trunk_closed_controller() # 트렁크 닫기

# execute_command瑜? ?젣?뼱?븯?뒗 肄쒕갚 ?븿?닔
# -> ?씠 ?븿?닔?뿉?꽌 ?떆洹몃꼸?쓣 ?엯?젰諛쏄퀬 泥섎━?븯?뒗 濡쒖쭅?쓣 援ъ꽦?븯硫?, ?븣?븘?꽌 GUI?뿉 ?뿰?룞?씠 ?맗?땲?떎.
def execute_command_callback(command, car_controller):
    executor = CarCommandExecutor(car_controller)
    executor.execute_command(command)


# ?뙆?씪 寃쎈줈瑜? ?엯?젰諛쏅뒗 ?븿?닔
# -> 媛?湲됱쟻 ?닔?젙?븯吏? 留덉꽭?슂.
#    ?뀒?뒪?듃?쓽 ?셿?쟾 ?옄?룞?솕 ?벑?쓣 ?쐞?븳 異붽?? 媛쒖꽑?떆?뿉留? ?씪遺? ?닔?젙?씠?슜?븯?떆硫? ?맗?땲?떎. (?꽦?쟻 諛섏쁺 X)
def file_input_thread(gui):
    while True:
        file_path = input("Please enter the command file path (or 'exit' to quit): ")

        if file_path.lower() == 'exit':
            print("Exiting program.")
            break

        # ?뙆?씪 寃쎈줈瑜? 諛쏆?? ?썑 GUI?쓽 mainloop?뿉?꽌 ?떎?뻾?븷 ?닔 ?엳?룄濡? ?걧?뿉 ?꽔?쓬
        gui.window.after(0, lambda: gui.process_commands(file_path))

# 硫붿씤 ?떎?뻾
# -> 媛?湲됱쟻 main login??? ?닔?젙?븯吏? 留덉꽭?슂.
if __name__ == "__main__":
    car = Car()
    car_controller = CarController(car)

    # GUI?뒗 硫붿씤 ?뒪?젅?뱶?뿉?꽌 ?떎?뻾
    gui = CarSimulatorGUI(car_controller, lambda command: execute_command_callback(command, car_controller))

    # ?뙆?씪 ?엯?젰 ?뒪?젅?뱶?뒗 蹂꾨룄濡? ?떎?뻾?븯?뿬, GUI??? 蹂묓뻾 泥섎━
    input_thread = threading.Thread(target=file_input_thread, args=(gui,))
    input_thread.daemon = True  # 硫붿씤 ?뒪?젅?뱶媛? 醫낅즺?릺硫? ?꽌釉? ?뒪?젅?뱶?룄 醫낅즺?릺?룄濡? ?꽕?젙
    input_thread.start()

    # GUI ?떆?옉 (硫붿씤 ?뒪?젅?뱶?뿉?꽌 ?떎?뻾)
    gui.start()