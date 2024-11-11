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

    def handle_acceleration(self):
     
        if self.car_controller.get_speed() < self.max_speed:
            self.car_controller.accelerate()
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

"""SOS 기능 제어 클래스"""
class SOSController:
    def __init__(self, car_controller):
        self.car_controller = car_controller

    def activate_sos(self):
        """SOS 기능: 차를 정지하고 모든 문을 열며 트렁크를 여는 기능"""
        print("SOS 기능이 활성화되었습니다: 차량이 정지되고, 모든 문이 열렸으며, 트렁크가 열렸습니다.")
        # 차량 정지
        while self.car_controller.get_speed() > 0:
            self.car_controller.brake()

        # 모든 문 잠금 해제
        self.car_controller.unlock_vehicle()
        self.car_controller.open_left_door()
        self.car_controller.open_right_door()
        # 트렁크 열기
        self.car_controller.open_trunk()
        # 엔진 끄기
        if self.car_controller.get_engine_status():
            self.car_controller.toggle_engine()

class CarCommandExecutor:
    def __init__(self, car_controller):
        self.engin_controller = EngineController(car_controller)
        self.movement_controller = MovementController(car_controller)
        self.sos_controller = SOSController(car_controller)
        self.car_controller = car_controller

    def execute_command(self, command):
        if command == "ENGINE_BTN":
            return self.engin_controller.handle_engine_control()
        
        elif command == "ACCELERATE":
            self.movement_controller.handle_acceleration()
        elif command == "BRAKE":
            self.movement_controller.handle_brake()
            
        elif command == "LOCK":
            self.car_controller.lock_vehicle()
        elif command == "UNLOCK":
            self.car_controller.unlock_vehicle()
            
        elif command == "LEFT_DOOR_LOCK":
            self.car_controller.lock_left_door()
        elif command == "LEFT_DOOR_UNLOCK":
            self.car_controller.unlock_left_door()
            
        elif command == "LEFT_DOOR_OPEN":
            self.car_controller.open_left_door()
        elif command == "LEFT_DOOR_CLOSE":
            self.car_controller.close_left_door()
            
        elif command == "TRUNK_OPEN":
            self.car_controller.open_trunk()
            
        elif command == "SOS":
            self.sos_controller.activate_sos()  # SOS 기능 호출

# execute_command를 제어하는 콜백 함수
def execute_command_callback(command, car_controller):
    executor = CarCommandExecutor(car_controller)
    executor.execute_command(command)

# 파일 경로를 입력받는 함수
def file_input_thread(gui):
    while True:
        file_path = input("Please enter the command file path (or 'exit' to quit): ")
        if file_path.lower() == 'exit':
            print("Exiting program.")
            break
        gui.window.after(0, lambda: gui.process_commands(file_path))

# 메인 실행
if __name__ == "__main__":
    car = Car()
    car_controller = CarController(car)
    gui = CarSimulatorGUI(car_controller, lambda command: execute_command_callback(command, car_controller))
    input_thread = threading.Thread(target=file_input_thread, args=(gui,))
    input_thread.daemon = True
    input_thread.start()
    gui.start()
