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
        엔진 제어 처리 하는 메서드
        Returns:
            엔진 제어 명령이 실행되었으면 True, 무시되었으면 False
        """
        current_speed = self.car_controller.get_speed()
        current_engin_status = self.car_controller.get_engine_status()
        # 주행 중이고 엔진이 켜져 있을 때 엔진 끄기 명령을 무시
        if current_speed > 0 and current_engin_status:
            print("\n[IGNORE]주행중이고 엔진이 켜져 있음")
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

    def handle_acceleration(self):
        """
        가속 처리
        Returns:
            가속 명령이 실행되었으면 True, 제한되었으면 False
        """
    def handle_break(self):
        """
        감속처리
        Returns:
            브레이크 명령이 실행되었으면 Treu, 제한되었으면 False
        """
class CarCommandExecutor:
    def __init__(self, car_controller):
        self.engin_controller = EngineController(car_controller)
        self.movement_controller = MovementController(car_controller)
        # ...
        self.car_controller = car_controller
    
    def execute_command(self, command):
        if command == "ENGINE_BTN":
            return self.engin_controller.handle_engine_control() # 시동 ON / OFF
        elif command == "ACCELERATE":
            car_controller.accelerate() # 속도 +10
        elif command == "BRAKE":
            car_controller.brake() # 속도 -10
        elif command == "LOCK":
            car_controller.lock_vehicle() # 차량잠금
        elif command == "UNLOCK":
            car_controller.unlock_vehicle() # 차량잠금해제
        elif command == "LEFT_DOOR_LOCK":
            car_controller.lock_left_door() # 왼쪽문 잠금
        elif command == "LEFT_DOOR_UNLOCK":
            car_controller.unlock_left_door() # 왼쪽문 잠금해제
        elif command == "LEFT_DOOR_OPEN":
            car_controller.open_left_door() # 왼쪽문 열기
        elif command == "LEFT_DOOR_CLOSE":
            car_controller.close_left_door() # 왼쪽문 닫기
        elif command == "TRUNK_OPEN":
            car_controller.open_trunk() # 트렁크 열기

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