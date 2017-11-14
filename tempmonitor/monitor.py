import json
import machine
import network
import umqtt.robust as mqtt

import hwconf
from tempmonitor import board

sta_if = network.WLAN(network.STA_IF)
default_config = {
    'topic': 'sensor',
    'interval': 60,
}


class Monitor():
    def __init__(self, config):
        self.config = default_config
        self.config.update(config)
        self.init_board()

    def init_board(self):
        self.board = board.Board()

    def run(self):
        self.board.led_on()

        try:
            self.init_network()
            self.init_mqtt()
            self.sample_and_report()
        except OSError as err:
            print('! failed to sample and report data ({})'.format(err))

        self.board.led_off()
        self.board.deepsleep(int(self.config['interval']))

    def sample_and_report(self):
        sample = self.board.read_dht()

        calibration = getattr(hwconf, 'calibration', {})
        for k in list(sample.keys()):
            cal = calibration.get(k, 0)
            print('# {} calibration = {}'.format(k, cal))
            sample['{}_raw'.format(k)] = sample[k]
            sample['{}_calibration'.format(k)] = cal
            sample[k] = sample['{}_raw'.format(k)] + cal

        sample.update(self.config.get('tags', {}))
        sample.update({
            'sensor_id': self.board.id(),
        })

        topic = '{topic}/dht/{id}'.format(
            id=self.board.id(), **self.config)
        value = json.dumps(sample)

        print('* reporting {} = {}'.format(topic, value))

        self.mqtt_client.publish(topic, value)
        self.mqtt_client.disconnect()

    def init_network(self):
        print('* configuring network')

        ap_if = network.WLAN(network.AP_IF)
        if ap_if.active():
            ap_if.active(False)

        if not sta_if.active():
            sta_if.active(True)

        if not sta_if.isconnected():
            sta_if.connect(self.config['ssid'])
            while not sta_if.isconnected():
                machine.idle()

        print('* configured with ip', sta_if.ifconfig()[0])

    def init_mqtt(self):
        server = self.config['mqtt_server']
        self.mqtt_id = 'sensor-{}'.format(self.board.id())

        print('* reporting to {} as {}'.format(server, self.mqtt_id))
        print('# connecting to mqtt server {}'.format(server))
        client = mqtt.MQTTClient(self.mqtt_id, self.config['mqtt_server'])
        client.connect()
        print('# connected to mqtt server {}'.format(server))

        self.mqtt_client = client
