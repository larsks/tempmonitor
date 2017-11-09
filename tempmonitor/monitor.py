import binascii
import dht
import machine
import network
import time
import umqtt.robust as mqtt

from machine import Pin

from tempmonitor import sleep

sta_if = network.WLAN(network.STA_IF)


class Monitor():
    def __init__(self, config):
        self.config = config
        self.init_dht()

    def run(self):
        self.init_network()
        self.init_mqtt()

        sample = next(self.sample())

        for k, v in sample.items():
            topic = 'sensor/{}/{}'.format(
                self.mqtt_id, k)
            value = bytes(str(v), 'utf8')

            print('* reporting {} = {}'.format(topic, value))
            self.mqtt_client.publish(topic, value)

        self.mqtt_client.disconnect()
        sleep.deepsleep(int(self.config['interval']))

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
        mac = sta_if.config('mac')
        server = self.config['mqtt_server']

        mqtt_id = binascii.hexlify(mac).decode('utf8')
        print('* reporting to {} as {}'.format(
            server, mqtt_id))

        print('# connecting to mqtt server {}'.format(server))
        client = mqtt.MQTTClient(mqtt_id,
                                 self.config['mqtt_server'])
        client.connect()
        print('# connected to mqtt server {}'.format(server))

        self.mqtt_client = client

    def init_dht(self):
        dht_pin = self.config['dht_pin']
        print('* temperature sensor on pin {}'.format(dht_pin))
        self.dht = dht.DHT(Pin(dht_pin))

    def sample(self):
        while True:
            try:
                self.dht.measure()
                tmp, hum = self.dht.temperature(), self.dht.humidity()
                print('# read temperature {}, humidity {}'
                      .format(tmp, hum))
                yield {
                    'temperature': tmp,
                    'humidity': hum,
                }
            except OSError:
                print('! failed to read dht22, retrying')

            time.sleep(2)

        print('* read temperature {}, humidity {}'.format(tmp, hum))
