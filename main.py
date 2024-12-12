import threading
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI


def execute_command_callback(command, car_controller):

    # 명령어를 공백 기준으로 분리
    commands = command.split()

        # 시동
    if "ENGINE_BTN" in commands:
        # ON: 브레이크 필요
        if not car_controller.get_engine_status():
            if "BRAKE" in commands and commands.index("BRAKE") < commands.index("ENGINE_BTN"):
                car_controller.toggle_engine()  # 엔진 켜기
            else:
                print("브레이크를 먼저 밟은 상태에서만 시동을 걸 수 있습니다.")
        # OFF: 바로 끌 수 있음
        else:
            if car_controller.get_speed() > 0:
                print("차량이 주행중이므로 시동을 끌 수 없습니다.")
            else:
                car_controller.toggle_engine()  # 엔진 끄기
                

#주행
    elif command == "ACCELERATE":
        if car_controller.get_engine_status():
            car_controller.accelerate()  # 속도 +10
        else:
            print("엔진이 꺼져 있어 가속할 수 없습니다.")
    elif command == "BRAKE":
        if car_controller.get_engine_status():
            car_controller.brake()
        else:
            print("엔진이 꺼져 있어 감속할 수 없습니다.")

#차량 전체 잠금
    elif command == "LOCK":
        if car_controller.get_left_door_status() == "CLOSED" and car_controller.get_right_door_status() == "CLOSED": 
            car_controller.lock_vehicle() # 차량잠금
    elif command == "UNLOCK":
        if car_controller.get_left_door_status() == "CLOSED" and car_controller.get_right_door_status() == "CLOSED": 
            car_controller.unlock_vehicle() # 차량잠금해제
        
#왼쪽 문
    elif command == "LEFT_DOOR_LOCK":
        car_controller.lock_left_door() # 왼쪽문 잠금
    elif command == "LEFT_DOOR_UNLOCK":
        car_controller.unlock_left_door() # 왼쪽문 잠금해제
        if car_controller.get_lock_status():
            car_controller.unlock_vehicle() # 차량 잠금도 해제
    elif command == "LEFT_DOOR_OPEN":
        if car_controller.get_left_door_lock() == "UNLOCKED":
            car_controller.open_left_door() # 왼쪽문 열기
        else :
            print("왼쪽 문이 잠겨있습니다.")
    elif command == "LEFT_DOOR_CLOSE":
        car_controller.close_left_door() # 왼쪽문 닫기

#오른쪽 문
    elif command == "RIGHT_DOOR_LOCK":
        car_controller.lock_right_door() # 오른문 잠금
    elif command == "RIGHT_DOOR_UNLOCK": 
        car_controller.unlock_right_door() # 오른문 잠금해제
        if car_controller.get_lock_status():
            car_controller.unlock_vehicle() # 차량 잠금도 해제
    elif command == "RIGHT_DOOR_OPEN":
        if car_controller.get_right_door_lock() == "UNLOCKED":
            car_controller.open_right_door() # 오른문 열기
        else :
            print("오른쪽 문이 잠겨있습니다.")
    elif command == "RIGHT_DOOR_CLOSE":
        car_controller.close_right_door() # 오른문 닫기
# 트렁크
    elif command == "TRUNK_OPEN":
        if car_controller.get_speed() > 0:
            print("차량이 주행 중이므로 트렁크를 열 수 없습니다.")
        else:
            car_controller.open_trunk() # 트렁크 열기

    elif command == "TRUNK_CLOSE":
        car_controller.close_trunk() # 트렁크 닫기
# SOS 기능
    elif command == "SOS":
        print("SOS 기능이 활성화되었습니다. 차량을 정지하고 문을 열고 트렁크를 엽니다.")
        
        # 차량 속도 0으로 설정
        while car_controller.get_speed() > 0:
            car_controller.brake()
        
        # 모든 문의 잠금 해제
        car_controller.unlock_vehicle()
        car_controller.unlock_left_door()
        car_controller.unlock_right_door()
        
        # 트렁크 열기
        car_controller.open_trunk()




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


import unittest
from unittest.mock import MagicMock
from car import Car
from car_controller import CarController
from main import execute_command_callback  # execute_command_callback 위치에 맞게 import


class TestCarController(unittest.TestCase):
    def setUp(self):
        # CarController 클래스의 인스턴스를 모킹합니다.
        self.car_controller = MagicMock()

    def test_01_engine_start_without_brake(self):
        # 1번: 브레이크를 밟지 않았을 때 시동을 걸 수 없도록 검증
        # 초기 엔진 상태는 꺼져 있고, 차량 속도는 0으로 설정
        self.car_controller.get_engine_status = MagicMock(return_value=False)
        self.car_controller.get_speed = MagicMock(return_value=0)

        # execute_command_callback("ENGINE_BTN") 호출
        execute_command_callback("ENGINE_BTN", self.car_controller)

        # `toggle_engine`이 호출되지 않아야 함
        self.car_controller.toggle_engine.assert_not_called()

    def test_02_engine_start_with_brake(self):
        # 2번: 브레이크를 밟았을 때 시동을 걸 수 있도록 검증
        self.car_controller.get_engine_status = MagicMock(return_value=False)
        self.car_controller.get_speed = MagicMock(return_value=0)

        # execute_command_callback("BRAKE ENGINE_BTN") 호출
        execute_command_callback("BRAKE ENGINE_BTN", self.car_controller)

        # `toggle_engine`이 호출되어야 함
        self.car_controller.toggle_engine.assert_called_once()

    def test_03_engine_stop_with_speed(self):
        # 3번: 차량이 주행 중일 때 시동을 끌 수 없음
        self.car_controller.get_engine_status = MagicMock(return_value=True)
        self.car_controller.get_speed = MagicMock(return_value=10)

        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.car_controller.toggle_engine.assert_not_called()

    def test_04_engine_stop_without_speed(self):
        # 4번: 차량이 정지 중일 때 시동을 끌 수 있음
        self.car_controller.get_engine_status = MagicMock(return_value=True)
        self.car_controller.get_speed = MagicMock(return_value=0)

        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.car_controller.toggle_engine.assert_called_once()

    def test_05_acceleration_when_engine_off(self):
        # 5번: 엔진이 꺼져 있을 때 가속 불가
        self.car_controller.get_engine_status = MagicMock(return_value=False)

        execute_command_callback("ACCELERATE", self.car_controller)
        self.car_controller.accelerate.assert_not_called()

    def test_06_acceleration_when_engine_on(self):
        # 6번: 엔진이 켜져 있을 때 가속 가능
        self.car_controller.get_engine_status = MagicMock(return_value=True)

        execute_command_callback("ACCELERATE", self.car_controller)
        self.car_controller.accelerate.assert_called_once()

    def test_07_lock_when_doors_open(self):
        # 7번: 문이 열려 있을 때 차량 잠금 불가
        self.car_controller.get_left_door_status = MagicMock(return_value="OPEN")
        self.car_controller.get_right_door_status = MagicMock(return_value="CLOSED")

        execute_command_callback("LOCK", self.car_controller)
        self.car_controller.lock_vehicle.assert_not_called()

    def test_08_lock_when_doors_closed(self):
        # 8번: 문이 닫혀 있을 때 차량 잠금 가능
        self.car_controller.get_left_door_status = MagicMock(return_value="CLOSED")
        self.car_controller.get_right_door_status = MagicMock(return_value="CLOSED")

        execute_command_callback("LOCK", self.car_controller)
        self.car_controller.lock_vehicle.assert_called_once()



if __name__ == "__main__":
    unittest.main()
