import threading
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI


# execute_command를 제어하는 콜백 함수
# -> 이 함수에서 시그널을 입력받고 처리하는 로직을 구성하면, 알아서 GUI에 연동이 됩니다.

def execute_command_callback(command, car_controller):
    if command == "ENGINE_BTN":
        car_controller.toggle_engine() # 시동 ON / OFF
#주행
    elif command == "ACCELERATE":
        if car_controller.get_engine_status():
            car_controller.accelerate()  # 속도 +10
        else:
            print("엔진이 꺼져 있어 가속할 수 없습니다.")
    elif command == "BRAKE":
        if car_controller.get_engine_status():
            car_controller.brake() # 속도 -10
        else:
            print("엔진이 꺼져 있어 감속할 수 없습니다.")
#차량 잠금
    elif command == "LOCK":
        if car_controller.get_left_door_status() == "CLOSED" and car_controller.get_right_door_status() == "CLOSED": 
            car_controller.lock_vehicle() # 차량잠금
            car_controller.lock_left_door()
            car_controller.lock_right_door()
        else:
            print("열린 문이 있습니다")
    elif command == "UNLOCK":
        if car_controller.get_left_door_status() == "CLOSED" and car_controller.get_right_door_status() == "CLOSED": 
            car_controller.unlock_vehicle() # 차량잠금해제
            car_controller.unlock_left_door()
            car_controller.unlock_right_door()
        else:
            print("열린 문이 있습니다")

#왼쪽 문
    elif command == "LEFT_DOOR_LOCK":
        if car_controller.get_left_door_status() == "CLOSED":
            car_controller.lock_left_door() # 왼쪽문 잠금
        else:
            print("왼쪽 문이 열려있습니다.")
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
        if car_controller.get_right_door_status() == "CLOSED":
            car_controller.lock_right_door()  # 왼쪽문 잠금
        else:
            print("오른쪽 문이 열려있습니다.")
        # 오른문 잠금
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
#트렁크
    elif command == "TRUNK_OPEN":
        car_controller.open_trunk() # 트렁크 열기
    elif command == "TRUNK_CLOSE":
        car_controller.open_trunk() # 닫기
#SOS
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

class TestCarControllerSOS(unittest.TestCase):
    def setUp(self):
        # 자동차와 CarController 인스턴스를 설정하고, 메서드들을 모킹하여 호출 여부를 확인할 수 있게 함
        self.car = Car()
        self.car_controller = CarController(self.car)

        # 각 메서드에 대해 모킹하여 호출 여부 확인
        self.car_controller.toggle_engine = MagicMock()
        self.car_controller.accelerate = MagicMock()
        self.car_controller.brake = MagicMock()
        self.car_controller.lock_vehicle = MagicMock()
        self.car_controller.unlock_vehicle = MagicMock()
        self.car_controller.lock_left_door = MagicMock()
        self.car_controller.unlock_left_door = MagicMock()
        self.car_controller.open_left_door = MagicMock()
        self.car_controller.close_left_door = MagicMock()
        self.car_controller.lock_right_door = MagicMock()
        self.car_controller.unlock_right_door = MagicMock()
        self.car_controller.open_right_door = MagicMock()
        self.car_controller.close_right_door = MagicMock()
        self.car_controller.open_trunk = MagicMock()
        self.car_controller.close_trunk = MagicMock()

    # 1. 시동 ON / OFF 테스트
    def test_toggle_engine(self):
        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.car_controller.toggle_engine.assert_called_once()

    # 2. 가속 테스트
    def test_accelerate(self):
        self.car_controller.get_engine_status = MagicMock(return_value=True)
        execute_command_callback("ACCELERATE", self.car_controller)
        self.car_controller.accelerate.assert_called_once()

    # 3. 감속 테스트
    def test_brake(self):
        self.car_controller.get_engine_status = MagicMock(return_value=True)
        execute_command_callback("BRAKE", self.car_controller)
        self.car_controller.brake.assert_called_once()

    # 4. 차량 잠금 테스트
    def test_lock_vehicle(self):
        self.car_controller.get_left_door_status = MagicMock(return_value="CLOSED")
        self.car_controller.get_right_door_status = MagicMock(return_value="CLOSED")
        execute_command_callback("LOCK", self.car_controller)
        self.car_controller.lock_vehicle.assert_called_once()
        self.car_controller.lock_left_door.assert_called_once()
        self.car_controller.lock_right_door.assert_called_once()

    # 5. 차량 잠금 해제 테스트
    def test_unlock_vehicle(self):
        self.car_controller.get_left_door_status = MagicMock(return_value="CLOSED")
        self.car_controller.get_right_door_status = MagicMock(return_value="CLOSED")
        execute_command_callback("UNLOCK", self.car_controller)
        self.car_controller.unlock_vehicle.assert_called_once()
        self.car_controller.unlock_left_door.assert_called_once()
        self.car_controller.unlock_right_door.assert_called_once()

    # 6. 왼쪽 문 잠금 테스트
    def test_lock_left_door(self):
        self.car_controller.get_left_door_status = MagicMock(return_value="CLOSED")
        execute_command_callback("LEFT_DOOR_LOCK", self.car_controller)
        self.car_controller.lock_left_door.assert_called_once()

    # 7. 왼쪽 문 잠금 해제 테스트
    def test_unlock_left_door(self):
        execute_command_callback("LEFT_DOOR_UNLOCK", self.car_controller)
        self.car_controller.unlock_left_door.assert_called_once()

    # 8. 왼쪽 문 열기 테스트
    def test_open_left_door(self):
        self.car_controller.get_left_door_lock = MagicMock(return_value="UNLOCKED")
        execute_command_callback("LEFT_DOOR_OPEN", self.car_controller)
        self.car_controller.open_left_door.assert_called_once()

    # 9. 왼쪽 문 닫기 테스트
    def test_close_left_door(self):
        execute_command_callback("LEFT_DOOR_CLOSE", self.car_controller)
        self.car_controller.close_left_door.assert_called_once()

    # 10. 오른쪽 문 잠금 테스트
    def test_lock_right_door(self):
        self.car_controller.get_right_door_status = MagicMock(return_value="CLOSED")
        execute_command_callback("RIGHT_DOOR_LOCK", self.car_controller)
        self.car_controller.lock_right_door.assert_called_once()

    # 11. 오른쪽 문 잠금 해제 테스트
    def test_unlock_right_door(self):
        execute_command_callback("RIGHT_DOOR_UNLOCK", self.car_controller)
        self.car_controller.unlock_right_door.assert_called_once()

    # 12. 오른쪽 문 열기 테스트
    def test_open_right_door(self):
        self.car_controller.get_right_door_lock = MagicMock(return_value="UNLOCKED")
        execute_command_callback("RIGHT_DOOR_OPEN", self.car_controller)
        self.car_controller.open_right_door.assert_called_once()

    # 13. 오른쪽 문 닫기 테스트
    def test_close_right_door(self):
        execute_command_callback("RIGHT_DOOR_CLOSE", self.car_controller)
        self.car_controller.close_right_door.assert_called_once()

    # 14. 트렁크 열기 테스트
    def test_open_trunk(self):
        execute_command_callback("TRUNK_OPEN", self.car_controller)
        self.car_controller.open_trunk.assert_called_once()

    # 15. 트렁크 닫기 테스트
    def test_close_trunk(self):
        execute_command_callback("TRUNK_CLOSE", self.car_controller)
        self.car_controller.close_trunk.assert_called_once()
        
    # 16. sos 테스트    
    def test_sos_function(self):

        # SOS 명령을 실행
        execute_command_callback("SOS", self.car_controller)

        # 차량 속도가 0으로 줄어드는지 확인
        self.car_controller.brake.assert_called()  # 브레이크가 호출되어야 함
        self.assertEqual(self.car_controller.get_speed(), 0)

        # 모든 문이 잠금 해제되었는지 확인
        self.car_controller.unlock_vehicle.assert_called_once()
        self.car_controller.unlock_left_door.assert_called_once()
        self.car_controller.unlock_right_door.assert_called_once()

        # 트렁크가 열렸는지 확인
        self.car_controller.open_trunk.assert_called_once()

if __name__ == "__main__":
    unittest.main()
