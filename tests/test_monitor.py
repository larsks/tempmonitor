from unittest import TestCase
from unittest.mock import MagicMock, patch


class TestSleep(TestCase):
    def setUp(self):
        self.mock_machine = MagicMock()
        self.mock_esp = MagicMock()
        self.mock_flashbdev = MagicMock()
        self.mock_dht = MagicMock()
        self.mock_network = MagicMock()
        self.mock_umqtt = MagicMock()
        self.mock_umqtt_robust = MagicMock()

        self.mock_Pin = MagicMock()
        self.mock_machine.Pin.return_value = self.mock_Pin

        self.mock_DHT22 = MagicMock()
        self.mock_dht.DHT22.return_value = self.mock_DHT22

        self.modules = {
            'machine': self.mock_machine,
            'esp': self.mock_esp,
            'flashbdev': self.mock_flashbdev,
            'dht': self.mock_dht,
            'network': self.mock_network,
            'umqtt': self.mock_umqtt,
            'umqtt.robust': self.mock_umqtt_robust,
        }

        self.module_patcher = patch.dict('sys.modules',
                                         self.modules)

    def test_init(self):
        with self.module_patcher:
            from tempmonitor import monitor

            config = {
                'dht_pin': 1,
            }

            monitor.Monitor(config)

            self.mock_machine.Pin.assert_called_with(
                config['dht_pin'])
            assert self.mock_dht.DHT22.called

    def test_sample(self):
        with self.module_patcher:
            from tempmonitor import monitor

            expected_tmp = 10
            expected_hum = 20

            self.mock_DHT22.temperature.return_value = expected_tmp
            self.mock_DHT22.humidity.return_value = expected_hum

            config = {
                'dht_pin': 1,
            }

            m = monitor.Monitor(config)
            s = next(m.sample())

            assert self.mock_DHT22.measure.called
            assert s['humidity'] == expected_hum
            assert s['temperature'] == expected_tmp
