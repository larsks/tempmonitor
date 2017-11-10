from unittest import TestCase
from unittest.mock import MagicMock, patch


class MPTestCase(TestCase):
    def setUp(self):
        self.mock_machine = MagicMock()
        self.mock_esp = MagicMock()
        self.mock_flashbdev = MagicMock()
        self.mock_dht = MagicMock()
        self.mock_network = MagicMock()
        self.mock_rtc = MagicMock()
        self.mock_umqtt = MagicMock()
        self.mock_umqtt_robust = MagicMock()

#        self.mock_Pin = MagicMock()
#        self.mock_machine.Pin.return_value = self.mock_Pin
#
#        self.mock_DHT22 = MagicMock()
#        self.mock_dht.DHT22.return_value = self.mock_DHT22
#
#        self.mock_machine.RTC.return_value = self.mock_rtc

        self.modules = {
            'machine': self.mock_machine,
            'esp': self.mock_esp,
            'flashbdev': self.mock_flashbdev,
            'dht': self.mock_dht,
            'network': self.mock_network,
            'rtc': self.mock_rtc,
            'umqtt': self.mock_umqtt,
            'umqtt.robust': self.mock_umqtt_robust,
        }

        self.module_patcher = patch.dict('sys.modules',
                                         self.modules)
