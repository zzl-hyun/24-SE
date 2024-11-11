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
                print("[IGNORE]오른쪽 문이 잠겨 있어 문 닫힘 상태 유지")
            # 오른쪽 문이 잠겨 있지 않을 때
            elif current_right_door_lock == "UNLOCKED":
                print("오른쪽 문 열림")
                self.car_controller.open_right_door()
        # 오른쪽 문이 열려 있을 때 오른쪽 문 열기 명령을 무시
        elif current_right_door_status == "OPEN":
            print("[IGNORE]오른쪽 문이 이미 열려 있음")

    def handle_left_door_open_controller(self):
        current_left_door_status = self.car_controller.get_left_door_status()
        current_left_door_lock = self.car_controller.get_left_door_lock()
        # 왼쪽 문이 닫혀 있을 때
        if current_left_door_status == "CLOSED":
            # 왼쪽 문이 잠겨 있을 때
            if current_left_door_lock == "LOCKED":
                print("[IGNORE]왼쪽 문이 잠겨 있어 문 닫힘 상태 유지")
            # 왼쪽 문이 잠겨 있지 않을 때
            elif current_left_door_lock == "UNLOCKED":
                print("왼쪽 문 열림")
                self.car_controller.open_left_door()
        # 왼쪽 문이 열려 있을 때 왼쪽 문 열기 명령을 무시
        elif current_left_door_status == "OPEN":
            print("[IGNORE]왼쪽 문이 이미 열려 있음")


# 문 닫기 클래스
class ClosedDoorController:
    def __init__(self, car_controller):
        self.car_controller = car_controller

    def handle_right_door_closed_controller(self):
        current_right_door_status = self.car_controller.get_right_door_status()
        # 오른쪽 문이 열려 있을 때
        # 잠겨 있든 아니든 문 닫기 가능
        if current_right_door_status == "OPEN":
            print("오른쪽 문 닫힘")
            self.car_controller.close_right_door()
        # 오른쪽 문이 닫혀 있을 때 오른쪽 문 닫기 명령을 무시
        elif current_right_door_status == "CLOSED":
            print("[IGNORE]오른쪽 문이 이미 닫혀 있음")

    def handle_left_door_closed_controller(self):
        current_left_door_status = self.car_controller.get_left_door_status()
        # 왼쪽 문이 열려 있을 때
        # 잠겨 있든 아니든 문 닫기 가능
        if current_left_door_status == "OPEN":
            print("왼쪽 문 닫힘")
            self.car_controller.close_left_door()
        # 왼쪽 문이 닫혀 있을 때 왼쪽 문 닫기 명령을 무시
        elif current_left_door_status == "CLOSED":
            print("[IGNORE]왼쪽 문이 이미 닫혀 있음")


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

class CarCommandExecutor:
    def __init__(self, car_controller):
        self.car_controller = car_controller
        self.door_open_controller = OpenDoorController(car_controller)
        self.door_closed_controller = ClosedDoorController(car_controller)
        self.trunk_controller = TrunkController(car_controller)

    def execute_command(self, command):
        if command == "ENGINE_BTN":
            car_controller.toggle_engine() # 시동 ON / OFF
        elif command == "ACCELERATE":
            car_controller.accelerate() # 속도 +10
        elif command == "BRAKE":
            car_controller.brake() # 속도 -10
        elif command == "LOCK":
            car_controller.lock_vehicle() # 차량 잠금
        elif command == "UNLOCK":
            car_controller.unlock_vehicle() # 차량 잠금 해제
        elif command == "LEFT_DOOR_LOCK":
            car_controller.lock_left_door() # 왼쪽문 잠금
        elif command == "LEFT_DOOR_UNLOCK":
            car_controller.unlock_left_door() # 왼쪽문 잠금 해제
        elif command == "RIGHT_DOOR_LOCK":
            car_controller.lock_right_door() # 오른쪽문 잠금
        elif command == "RIGHT_DOOR_UNLOCK":
            car_controller.unlock_right_door() # 오른쪽문 잠금 해제
        elif command == "LEFT_DOOR_OPEN":
            return self.door_open_controller.handle_left_door_open_controller() # 왼쪽문 열기
        elif command == "LEFT_DOOR_CLOSE":
            return self.door_closed_controller.handle_left_door_closed_controller() # 왼쪽문 닫기
        elif command == "right_DOOR_OPEN":
            return self.door_open_controller.handle_right_door_open_controller() # 오른쪽 문 열기
        elif command == "right_DOOR_CLOSE":
            return self.door_closed_controller.handle_right_door_closed_controller() # 오른쪽 문 닫기
        elif command == "TRUNK_OPEN":
            return self.trunk_controller.handle_trunk_open_controller() # 트렁크 열기
        elif command == "TRUNK_CLOSED":
            return self.trunk_controller.handle_trunk_closed_controller() # 트렁크 닫기



# execute_command를 제어하는 콜백 함수
# -> 이 함수에서 시그널을 입력받고 처리하는 로직을 구성하면, 알아서 GUI에 연동이 됩니다.

def execute_command_callback(command, car_controller):
    executor = CarCommandExecutor(car_controller)
    executor.execute_command(command)



# 파일 경로를 입력받는 함수
# -> 가급적 수정하지 마세요.
#    테스트의 완전 자동화 등을 위한 추가 개선시에만 일부 수정이용하시면 됩니다. (성적 반영 X)
def file_input_thread(gui):
    while True:
        file_path = input("Please enter the command file path (or 'exit' to quit): ")

        if file_path.lower() == 'exit':
            print("Exiting program.")
            break

        # 파일 경로를 받은 후 GUI의 mainloop에서 실행할 수 있도록 큐에 넣음
        gui.window.after(0, lambda: gui.process_commands(file_path))

# 메인 실행
# -> 가급적 main login은 수정하지 마세요.
if __name__ == "__main__":
    car = Car()
    car_controller = CarController(car)

    # GUI는 메인 스레드에서 실행
    gui = CarSimulatorGUI(car_controller, lambda command: execute_command_callback(command, car_controller))

    # 파일 입력 스레드는 별도로 실행하여, GUI와 병행 처리
    input_thread = threading.Thread(target=file_input_thread, args=(gui,))
    input_thread.daemon = True  # 메인 스레드가 종료되면 서브 스레드도 종료되도록 설정
    input_thread.start()

    # GUI 시작 (메인 스레드에서 실행)
    gui.start()