import threading
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI
import unittest

"""
openClose.py    문 열기/닫기 제어(4~5), 트렁크 제어
lock.py         문 잠금 제어(6~8)
engineSpeed.py  엔진제어(1~2) 속도 제어(9~10)
additional.py   추가 기능 

# 발견한 문제
1. 서로 연관된 컨트롤러 전달해야 할 듯?
ex) sos : lock, open, trunk, engine, speed 다 관여 


# 유닛테스팅 수행
SOS 기능에 대한 테스트 코드 작성 후 프로젝트에 포함시킬 것 (unittest 라이브러리 이용할 것)

그 외 기능에 대해, 최소 1개의 테스트 케이스를 만들어서 프로젝트에 포함시킬 것


# 수정 완
1. handle_acceleration() 함수 중복
2. ALL_DOOR_LOCK, ALL_DOOR_UNLOCK -> UNLOCK, LOCK 으로 수정해야함 (input 조건 안맞음)
3. CarCommandExecutor __init__ 수정 필요   EngineController(car_controller)  -> EngineController(self.car_controller) self.로 바꿔야 함

1. SOS 실행 시 문이 LOCKED에서도 열림
 -> 서로 연관된 컨트롤러 전달해야 할 듯?
    ex) sos : lock, open, trunk, engine, speed 다 관여 
2. trunkcontroller의 self.current_speed = self.car_controller.get_speed() 제거
    시점이 다름 self.car_controller.get_speed()로 실시간으로 확인해야함

"""



"""차량 엔진 제어 관련 클래스"""
## 변경 없음
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


"""SOS 기능 제어 클래스"""
## addional.py 
class SOSController:

    def __init__(self, car_controller, movement_controller, doorLock_controller, door_open_controller, trunk_controller, engin_controller):
        self.car_controller = car_controller
        ## 컨트롤러 추가했음
        self.movement_controller = movement_controller
        self.doorLock_controller = doorLock_controller
        self.door_open_controller = door_open_controller
        self.trunk_controller = trunk_controller
        self.engin_controller = engin_controller

    def activate_sos(self):
        """SOS 기능: 차를 정지하고 모든 문을 열며 트렁크를 여는 기능"""
        print("SOS 기능이 활성화되었습니다: 차량이 정지되고, 모든 문이 열렸으며, 트렁크가 열렸습니다.")
        # 차량 정지
        while self.car_controller.get_speed() > 0:
            # self.car_controller.brake()
            self.movement_controller.handle_brake()

        # 모든 문 잠금 해제
        # self.car_controller.unlock_vehicle()
        # print(self.car_controller.get_lock_status())
        # self.car_controller.open_left_door()
        # self.car_controller.open_right_door()
        self.doorLock_controller.allDoor_unLock()
        self.door_open_controller.handle_left_door_open_controller()
        self.door_open_controller.handle_right_door_open_controller()

        # 트렁크 열기
        # self.car_controller.open_trunk()
        self.trunk_controller.handle_trunk_open_controller()
        # 엔진 끄기
        if self.car_controller.get_engine_status():
            # self.car_controller.toggle_engine()
            self.engin_controller.handle_engine_control()
       

"""차량 이동 제어 관련 클래스"""
 ## lock.py, engineSpeed.py handle_acceleration() 함수 중복
class MovementController:
    def __init__(self, car_controller):
        self.car_controller = car_controller
        self.min_speed = 0
        self.max_speed = 200 # 최대 속도 제한

        """속도 감응식 자동 문 잠금처리 """ 
    def autoLock_by_speed(self): # lock.py
        """get_lock_status()이 False라면 차량의 문이 하나라도 열려있다는 뜻 -> 함수 실행"""
        if self.car_controller.get_lock_status() == False:
            self.car_controller.unlock_left_door()
            self.car_controller.unlock_right_door()
            self.car_controller.lock_vehicle()
            print("[속도 감응식 문 잠금]")
            
            
    # ## lock.py, engineSpeed.py handle_acceleration() 함수 중복
    # def handle_acceleration(self): #lock.py

    #     if self.car_controller.get_speed() < self.max_speed:
    #         self.car_controller.accelerate()
    #         if self.car_controller.get_speed() >= 15:
    #             self.autoLock_by_speed()
    #         return True
    #     print("속도가 최대값에 도달하여 가속할 수 없습니다.")
    #     return False
    
    ## lock.py, engineSpeed.py handle_acceleration() 함수 중복
    def handle_acceleration(self): # engineSpeed.py

        current_engin_status = self.car_controller.get_engine_status()

        if current_engin_status:
            if self.car_controller.get_speed() < self.max_speed:
                self.car_controller.accelerate()
                ## lock.py의 속도감응식 뭐시기 추가
                if self.car_controller.get_speed() >= 15:
                    self.autoLock_by_speed()
                return True
            print("[IGNORE] 차량이 최고 속도에 도달함")
            return False
        print("[IGNORE] 차량의 엔진이 꺼져있음")
        return False
    
    def handle_brake(self): # engineSpeed.py
        """
        감속 처리
        Returns:
            브레이크 명령이 실행되었으면 True, 제한되었으면 False
        """
        if self.car_controller.get_speed() > self.min_speed:
            self.car_controller.brake()
            ## debug
            print(f"감속됨 {self.car_controller.get_speed()}")
            return True
        print("[IGNORE] 차량이 정차 중임")
        return False

# 문 잠금 클래스
## lock.py
class DoorLockController:
    def __init__(self, car_controller):
        self.car_controller = car_controller

    """문 제어 시도시 print 출력"""
    def Lock_success(self, tryCase):
        print("[{} - 성공]".format(tryCase))

    def Lock_fail(self, tryCase, failReason):
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
    # 좌/우 문이 모두 닫혀있는지 확인 return True/False
    def get_allDoor_checking(self):
        if self.car_controller.get_left_door_status() == "CLOSED" and self.car_controller.get_right_door_status() == "CLOSED":
            return True
        else:
            return False
        
        # 수정 제시
        # return (self.car_controller.get_left_door_status() == "CLOSED" and self.car_controller.get_right_door_status() == "CLOSED")

        
    """
    각 함수 종료 시 차량이 잠금 상태인지 잠금 해제 된 상태인지 체크 후 Vehicle Locked/Unlocked 표시
    (기존의 <command : LOCK, UNLOCK> 대체)
    """
    # 차랑의 잠금상태 업데이트?
    def vehicle_statusChecking(self):
        if self.car_controller.get_left_door_lock() == "LOCKED" and self.car_controller.get_right_door_lock() == "LOCKED":
            self.car_controller.lock_vehicle()
        else:
            self.car_controller.unlock_vehicle()
            
    def allDoor_Lock(self):
        tryCase = "모든 문 잠금 시도"

        if self.get_allDoor_checking(): # 좌/우 문이 모두 닫혀있는지 확인
            if self.car_controller.get_left_door_lock() == "LOCKED" and self.car_controller.get_right_door_lock() == "LOCKED":
                self.Lock_fail(tryCase, "이미 모든 문이 잠긴 상태입니다.")
            else:
                self.car_controller.lock_left_door()
                self.car_controller.lock_right_door()
                self.Lock_success(tryCase)
        else:
            self.doorOpenStatus(tryCase)

        self.vehicle_statusChecking()

    def allDoor_unLock(self):
        tryCase = "모든 문 잠금 해제 시도"

        if self.car_controller.get_speed() != 0:
            self.Lock_fail(tryCase, "차량이 주행 중입니다.")
        elif self.get_allDoor_checking():
            if self.car_controller.get_left_door_lock() == "UNLOCKED" and self.car_controller.get_right_door_lock() == "UNLOCKED":
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
            if self.car_controller.get_left_door_lock() == "LOCKED":
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
            if self.car_controller.get_left_door_lock() == "UNLOCKED":
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
            if self.car_controller.get_right_door_lock() == "LOCKED":
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
            if self.car_controller.get_right_door_lock() == "UNLOCKED":
                self.Lock_fail(tryCase, "이미 오른쪽 문이 잠금 해제된 상태입니다.")
            else:
                self.Lock_success(tryCase)

                self.car_controller.unlock_right_door()
        else:
            self.doorOpenStatus(tryCase)

        self.vehicle_statusChecking()

# 문 열기 클래스
## openClose.py
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
# openClose.py
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
# openClose.py
class TrunkController:
    def __init__(self, car_controller):
        self.car_controller = car_controller
        self.trunk_status = self.car_controller.get_trunk_status()
        # self.current_speed = self.car_controller.get_speed()

    # 트렁크 열기
    def handle_trunk_open_controller(self):
        # 차가 정차 중 일때
        # if self.current_speed == 0:
        if self.car_controller.get_speed() == 0:
            # 트렁크가 닫혀 있으면(trunk_status=true)
            if self.trunk_status:
                self.car_controller.open_trunk()
                print("트렁크 열림")
            # 트렁크가 열려 있으면
            else:
                print("[IGNORE] 트렁크가 이미 열려 있음")
        # 차가 주행 중 일때
        # elif self.current_speed > 0:
        elif self.car_controller.get_speed() > 0:
            ##debug
            print(self.current_speed)
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
        self.engin_controller = EngineController(self.car_controller)
        self.movement_controller = MovementController(self.car_controller)
        self.doorLock_controller = DoorLockController(self.car_controller) # lock.py
        self.door_open_controller = OpenDoorController(self.car_controller) # openClose.py
        self.door_closed_controller = ClosedDoorController(self.car_controller) # openClose.py
        self.trunk_controller = TrunkController(self.car_controller) # openClose.py
        # self.sos_controller = SOSController(self.car_controller) # addional.py
        self.sos_controller = SOSController(
            self.car_controller,
            self.movement_controller,
            self.doorLock_controller,
            self.door_open_controller,
            self.trunk_controller,
            self.engin_controller
        )
    
    def execute_command(self, command):
        if command == "ENGINE_BTN":
            return self.engin_controller.handle_engine_control() # 시동 ON / OFF
        
        ## engineSpeed.py
        elif command == "ACCELERATE":
            self.movement_controller.handle_acceleration() # 속도 +10 /engineSpeed.py
        elif command == "BRAKE":
            self.movement_controller.handle_brake() # 속도 -10 /engineSpeed.py
            
        ## lock.py 
        # ALL_DOOR_LOCK, ALL_DOOR_UNLOCK -> UNLOCK, LOCK 으로 수정해야함 (input 조건 안맞음)
        # elif command == "ALL_DOOR_LOCK":
        #     self.doorLock_controller.allDoor_Lock()
        # elif command == "ALL_DOOR_UNLOCK":
        #     self.doorLock_controller.allDoor_unLock()
        elif command == "LOCK":
            self.doorLock_controller.allDoor_Lock()
        elif command == "UNLOCK":
            self.doorLock_controller.allDoor_unLock()
            
        elif command == "LEFT_DOOR_LOCK":
            self.doorLock_controller.leftDoor_Lock()
        elif command == "LEFT_DOOR_UNLOCK":
            self.doorLock_controller.leftDoor_unLock()
            
        elif command == "RIGHT_DOOR_LOCK":
            self.doorLock_controller.rightDoor_Lock()
        elif command == "RIGHT_DOOR_UNLOCK":
            self.doorLock_controller.rightDoor_unLock()
        
        ## openClose.py
        elif command == "LEFT_DOOR_OPEN":
            return self.door_open_controller.handle_left_door_open_controller() # 왼쪽문 열기
        elif command == "LEFT_DOOR_CLOSE":
            return self.door_closed_controller.handle_left_door_closed_controller() # 왼쪽문 닫기
        elif command == "RIGHT_DOOR_OPEN":
            return self.door_open_controller.handle_right_door_open_controller() # 오른쪽 문 열기
        elif command == "RIGHT_DOOR_CLOSE":
            return self.door_closed_controller.handle_right_door_closed_controller() # 오른쪽 문 닫기
        elif command == "TRUNK_OPEN":
            return self.trunk_controller.handle_trunk_open_controller() # 트렁크 열기
        elif command == "TRUNK_CLOSED":
            return self.trunk_controller.handle_trunk_closed_controller() # 트렁크 닫기

        ## addional.py
        elif command == "SOS":
            self.sos_controller.activate_sos()  # SOS 기능 호출
        else:
            print("잘못된 입력입니다.")
            return




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