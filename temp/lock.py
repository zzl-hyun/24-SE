import threading
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI

"""차량 엔진 제어 관련 클래스"""
class EngineController:
    def __init__(self, car_controller):
        self.car_controller = car_controller

    def handle_engine_control(self):
        """
        엔진 제어 처리하는 메서드
        Returns:
            엔진 제어 명령이 실행되었으면 True, 무시되었으면 False
        """
        current_speed = self.car_controller.get_speed()
        current_engin_status = self.car_controller.get_engine_status()
        # 주행 중이고 엔진이 켜져 있을 때 엔진 끄기 명령을 무시
        if current_speed > 0 and current_engin_status:
            print("\n[IGNORE] 주행 중이고 엔진이 켜져 있음")
            return False
        # 정차 중이거나 엔진이 꺼져있을 때만 엔진 상태 토글
        self.car_controller.toggle_engine()
        return True

"""차량 이동 제어 관련 클래스"""
class MovementController:
    def __init__(self, car_controller):
        self.car_controller = car_controller
        self.min_speed = 0
        self.max_speed = 200 # 최대 속도 제한

    """속도 감응식 자동 문 잠금처리"""
    def autoLock_by_speed(self):
        """get_lock_status()이 False라면 차량의 문이 하나라도 열려있다는 뜻 -> 함수 실행"""
        if self.car_controller.get_lock_status() == False:
            self.car_controller.unlock_left_door()
            self.car_controller.unlock_right_door()

            self.car_controller.lock_vehicle()
            print("[속도 감응식 문 잠금]")

    def handle_acceleration(self):
        """
        가속 처리
        Returns:
            가속 명령이 실행되었으면 True, 제한되었으면 False
        """
        if self.car_controller.get_speed() < self.max_speed:
            self.car_controller.accelerate()
            if self.car_controller.get_speed() >= 15:
                self.autoLock_by_speed()
            return True
        print("속도가 최대값에 도달하여 가속할 수 없습니다.")
        return False

    def handle_brake(self):
        """
        감속 처리
        Returns:
            브레이크 명령이 실행되었으면 True, 제한되었으면 False
        """
        if self.car_controller.get_speed() > self.min_speed:
            self.car_controller.brake()
            return True
        print("속도가 0이라 감속할 수 없습니다.")
        return False
    
"""차량 문 잠금 제어 관련 클래스"""
class DoorLockController:
    def __init__(self, car_controller):
        self.car_controller = car_controller

    """문 제어 시도시 print 출력"""
    def Lock_success(tryCase):
        print("[{} - 성공]".format(tryCase))

    def Lock_fail(tryCase, failReason):
        print("[{} - 실패] : {}".format(tryCase, failReason))

    """문이 열려있어서 잠금/잠금해제 실패한 경우"""
    def doorOpenStatus(self, tryCase):
        if self.car_controller.get_left_door_status() == "OPEN" and self.car_controller.get_right_door_status() == "OPEN":
            self.Lock_fail(tryCase, "모든 문이 열려있습니다")
        elif self.car_controller.get_left_door_status() == "OPEN":
            self.Lock_fail(tryCase, "왼쪽 문이 열려있습니다")
        elif self.car_controller.get_right_door_status() == "OPEN":
            self.Lock_fail(tryCase, "오른쪽 문이 열려있습니다")

    """모든/좌/우 문 잠금/잠금해제 시 모든 precondition이 차량의 모든 문이 잠긴 상태"""
    def get_allDoor_checking(self):
        if self.car_controller.get_left_door_status() == "CLOSED" and self.car_controller.get_right_door_status() == "CLOSED":
            return True
        else:
            return False
        
    """
    각 함수 종료 시 차량이 잠금 상태인지 잠금 해제 된 상태인지 체크 후 Vehicle Locked/Unlocked 표시
    (기존의 <command : LOCK, UNLOCK> 대체)
    """
    def vehicle_statusChecking(self):
        if self.car_controller.get_left_door_lock == "LOCKED" and self.car_controller.get_right_door_lock() == "LOCKED":
            self.car_controller.lock_vehicle()
        else:
            self.car_controller.unlock_vehicle()

    def allDoor_Lock(self):
        tryCase = "모든 문 잠금 시도"

        if self.get_allDoor_checking():
            if self.car_controller.get_left_door_lock == "LOCKED" and self.car_controller.get_right_door_lock() == "LOCKED":
                self.Lock_fail(tryCase, "이미 모든 문이 잠긴 상태입니다.")
            else:
                self.Lock_success(tryCase)
                
                self.car_controller.lock_left_door()
                self.car_controller.lock_right_door()
        else:
            self.doorOpenStatus(tryCase)

        self.vehicle_statusChecking()

    def allDoor_unLock(self):
        tryCase = "모든 문 잠금 해제 시도"

        if self.car_controller.get_speed() != 0:
            self.Lock_fail(tryCase, "차량이 주행 중입니다.")
        elif self.get_allDoor_checking():
            if self.car_controller.get_left_door_lock == "UNLOCKED" and self.car_controller.get_right_door_lock() == "UNLOCKED":
                self.Lock_fail(tryCase, "이미 모든 문이 잠금 해제된 상태입니다.")
            else:
                self.Lock_success(tryCase)

                self.car_controller.unlock_left_door()
                self.car_controller.unlock_right_door()
        else:
            self.doorOpenStatus(tryCase)

        self.vehicle_statusChecking()

    def leftDoor_Lock(self):
        tryCase = "왼쪽 문 잠금 시도"

        if self.get_allDoor_checking():
            if self.car_controller.get_left_door_lock == "LOCKED":
                self.Lock_fail(tryCase, "이미 왼쪽 문이 잠긴 상태입니다.")
            else:
                self.Lock_success(tryCase)
                
                self.car_controller.lock_left_door()
        else: 
            self.doorOpenStatus(tryCase)

        self.vehicle_statusChecking()

    def leftDoor_unLock(self):
        tryCase = "왼쪽 문 잠금 해제 시도"

        if self.car_controller.get_speed() != 0:
            self.Lock_fail(tryCase, "차량이 주행 중입니다.")
        elif self.get_allDoor_checking():
            if self.car_controller.get_left_door_lock == "UNLOCKED":
                self.Lock_fail(tryCase, "이미 왼쪽 문이 잠금 해제된 상태입니다.")
            else:
                self.Lock_success(tryCase)

                self.car_controller.unlock_left_door()
        else:
            self.doorOpenStatus(tryCase)

        self.vehicle_statusChecking()

    def rightDoor_Lock(self):
        tryCase = "오른쪽 문 잠금 시도"

        if self.get_allDoor_checking():
            if self.car_controller.get_right_door_lock == "LOCKED":
                self.Lock_fail(tryCase, "이미 오른쪽 문이 잠긴 상태입니다.")
            else:
                self.Lock_success(tryCase)
                
                self.car_controller.lock_right_door()
        else: 
            self.doorOpenStatus(tryCase)

        self.vehicle_statusChecking()

    def rightDoor_unLock(self):
        tryCase = "오른쪽 문 잠금 해제 시도"

        if self.car_controller.get_speed() != 0:
            self.Lock_fail(tryCase, "차량이 주행 중입니다.")
        elif self.get_allDoor_checking():
            if self.car_controller.get_right_door_lock == "UNLOCKED":
                self.Lock_fail(tryCase, "이미 오른쪽 문이 잠금 해제된 상태입니다.")
            else:
                self.Lock_success(tryCase)

                self.car_controller.unlock_right_door()
        else:
            self.doorOpenStatus(tryCase)

        self.vehicle_statusChecking()

class CarCommandExecutor:
    def __init__(self, car_controller):
        self.engin_controller = EngineController(car_controller)
        self.movement_controller = MovementController(car_controller)
        self.doorLock_controller = DoorLockController(car_controller)
        self.car_controller = car_controller

    """
    기존의 LOCK, UNLOCK command삭제 -> 
    각 잠금/잠금해제 후 차량의 문 잠금상태를 체크 후 Vehicle Locked/Unlocked 표시하도록 변경"""
    def execute_command(self, command):
        if command == "ENGINE_BTN":
            return self.engin_controller.handle_engine_control()
        elif command == "ACCELERATE":
            self.movement_controller.handle_acceleration()
        elif command == "BRAKE":
            self.movement_controller.handle_brake()
        
        elif command == "ALL_DOOR_LOCK":
            self.doorLock_controller.allDoor_Lock()
        elif command == "ALL_DOOR_UNLOCK":
            self.doorLock_controller.allDoor_unLock()
        elif command == "LEFT_DOOR_LOCK":
            self.doorLock_controller.leftDoor_Lock()
        elif command == "LEFT_DOOR_UNLOCK":
            self.doorLock_controller.leftDoor_unLock()
        elif command == "RIGHT_DOOR_UNLOCK":
            self.doorLock_controller.rightDoor_Lock()
        elif command == "RIGHT_DOOR_LOCK":
            self.doorLock_controller.rightDoor_unLock()
        
        elif command == "LEFT_DOOR_OPEN":
            self.car_controller.open_left_door()
        elif command == "LEFT_DOOR_CLOSE":
            self.car_controller.close_left_door()
        elif command == "TRUNK_OPEN":
            self.car_controller.open_trunk()

# execute_command를 제어하는 콜백 함수
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