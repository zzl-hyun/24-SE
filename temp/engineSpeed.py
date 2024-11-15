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
        """
        가속 처리
        Returns:
            가속 명령이 실행되었으면 True, 제한되었으면 False
        """
        current_engin_status = self.car_controller.get_engine_status()

        if current_engin_status:
            if self.car_controller.get_speed() < self.max_speed:
                self.car_controller.accelerate()
                return True
            print("[IGNORE] 차량이 최고 속도에 도달함")
            return False
        print("[IGNORE] 차량의 엔진이 꺼져있음")
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
        print("[IGNORE] 차량이 정차 중임")
        return False

class CarCommandExecutor:
    def __init__(self, car_controller):
        self.engin_controller = EngineController(car_controller)
        self.movement_controller = MovementController(car_controller)
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


