from unittest import TestCase
from unittest.mock import MagicMock, patch


class TestSleep(TestCase):
    def setUp(self):
        self.mock_machine = MagicMock()
        self.mock_esp = MagicMock()
        self.mock_flashbdev = MagicMock()

        self.modules = {
            'machine': self.mock_machine,
            'esp': self.mock_esp,
            'flashbdev': self.mock_flashbdev
        }

        self.module_patcher = patch.dict('sys.modules',
                                         self.modules)

    def test_enable_battery_monitor(self):
        with self.module_patcher:
            from tempmonitor import battery

            init_data = [0] * 108
            expected_data = init_data[:]
            expected_data[107] = battery.ADC_MODE_VCC
            sec_size = 10
            flash_size = 100

            self.mock_esp.flash_read.return_value = init_data
            self.mock_esp.flash_size.return_value = flash_size
            self.mock_flashbdev.SEC_SIZE = sec_size

            battery.enable_battery_monitor()

            assert (self.mock_esp.flash_write.call_args[0][1] ==
                    bytearray(expected_data))

    def test_enable_battery_monitor_when_enabled(self):
        with self.module_patcher:
            from tempmonitor import battery

            init_data = [0] * 108
            init_data[107] = battery.ADC_MODE_VCC
            expected_data = init_data[:]
            expected_data[107] = battery.ADC_MODE_VCC
            sec_size = 10
            flash_size = 100

            self.mock_esp.flash_read.return_value = init_data
            self.mock_esp.flash_size.return_value = flash_size
            self.mock_flashbdev.SEC_SIZE = sec_size

            battery.enable_battery_monitor()

            self.mock_esp.flash_write.assert_not_called

    def test_disable_battery_monitor(self):
        with self.module_patcher:
            from tempmonitor import battery

            init_data = [0] * 108
            expected_data = init_data[:]
            init_data[107] = battery.ADC_MODE_VCC
            sec_size = 10
            flash_size = 100

            self.mock_esp.flash_read.return_value = init_data
            self.mock_esp.flash_size.return_value = flash_size
            self.mock_flashbdev.SEC_SIZE = sec_size

            battery.disable_battery_monitor()

            assert (self.mock_esp.flash_write.call_args[0][1] ==
                    bytearray(expected_data))

    def test_disable_battery_monitor_when_disabled(self):
        with self.module_patcher:
            from tempmonitor import battery

            init_data = [0] * 108
            # expected_data = init_data[:]
            sec_size = 10
            flash_size = 100

            self.mock_esp.flash_read.return_value = init_data
            self.mock_esp.flash_size.return_value = flash_size
            self.mock_flashbdev.SEC_SIZE = sec_size

            battery.disable_battery_monitor()

            self.mock_esp.flash_write.assert_not_called
