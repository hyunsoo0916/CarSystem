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

        # execute_command_callback("ENGINE_BTN BRAKE") 호출
        execute_command_callback("ENGINE_BTN BRAKE", self.car_controller)

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
