import machine
import network
import umqtt.robust as mqtt

from tempmonitor import board
from tempmonitor.common import macaddr

sta_if = network.WLAN(network.STA_IF)


class Monitor():
    def __init__(self, config):
        self.config = config
        self.init_board()

    def run(self):
        self.board.led_on()
        self.init_network()
        self.init_mqtt()

        try:
            self.sample_and_report()
        except OSError as err:
            print('! failed to sample and report data ({})'.format(err))

        self.board.led_off()
        self.board.deepsleep(int(self.config['interval']))

    def sample_and_report(self):
        sample = self.board.read_dht()

        for k, v in sample.items():
            if 'calibration' in self.config:
                cal = self.config['calibration'].get(k, 0)
                print('# calibration = {}'.format(cal))
                v += cal

            topic = 'sensor/{}/{}'.format(
                self.mqtt_id, k)
            value = bytes(str(v), 'utf8')

            print('* reporting {} = {}'.format(topic, value))

            try:
                self.mqtt_client.publish(topic, value)
            except OSError:
                print('! failed to publish data')

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
        self.mqtt_id = macaddr()
        print('* reporting to {} as {}'.format(
            server, self.mqtt_id))

        print('# connecting to mqtt server {}'.format(server))
        client = mqtt.MQTTClient(self.mqtt_id,
                                 self.config['mqtt_server'])
        client.connect()
        print('# connected to mqtt server {}'.format(server))

        self.mqtt_client = client

    def init_board(self):
        self.board = board.Board()
