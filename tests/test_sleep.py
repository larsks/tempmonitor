from unittest import TestCase
from unittest.mock import MagicMock, patch


class TestSleep(TestCase):
    def setUp(self):
        self.mock_machine = MagicMock()
        self.mock_rtc = MagicMock()
        self.mock_machine.RTC.return_value = self.mock_rtc

        self.modules = {
            'machine': self.mock_machine,
        }

        self.module_patcher = patch.dict('sys.modules',
                                         self.modules)

    def test_deepsleep(self):
        with self.module_patcher:
            from tempmonitor import sleep
            sleeptime = 10

            sleep.deepsleep(sleeptime)

            self.mock_rtc.alarm.assert_called_with(
                self.mock_rtc.ALARM0, sleeptime * 1000)

    def test_deepsleep_ms(self):
        with self.module_patcher:
            from tempmonitor import sleep
            sleeptime = 10

            sleep.deepsleep_ms(sleeptime)

            self.mock_rtc.alarm.assert_called_with(
                self.mock_rtc.ALARM0, sleeptime)
