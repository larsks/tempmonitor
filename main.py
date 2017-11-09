import dht
import json
import machine
import network
import sys
import time
import ubinascii as binascii
import umqtt.robust as mqtt

import sleep

try:
    with open('config.json') as fd:
        config = json.load(fd)
except OSError:
    print('configuration is not available')
    sys.exit()


def configure_network():
    global config
    global sta_if

    print('* configuring network')

    ap_if = network.WLAN(network.AP_IF)
    sta_if.active(True)
    ap_if.active(False)

    sta_if.connect(config['ssid'])

    while not sta_if.isconnected():
        machine.idle()

    print('* configured with ip', sta_if.ifconfig()[0])


def read_dht22(dev):
    time.sleep(2)

    while True:
        try:
            dev.measure()
            break
        except OSError:
            print('! failed to read dht22, retrying')
            time.sleep(2)

    tmp, hum = dev.temperature(), dev.humidity()
    print('* read temperature {}, humidity {}'.format(tmp, hum))
    return tmp, hum


sta_if = network.WLAN(network.STA_IF)

if not sta_if.isconnected():
    configure_network()

mac = sta_if.config('mac')
mqtt_id = binascii.hexlify(mac).decode('utf8')

print('* reporting to {mqtt_server}'.format(**config))
print('* reporting as {}'.format(mqtt_id))

dev = dht.DHT22(machine.Pin(config['dht_pin']))
samples = (read_dht22(dev), read_dht22(dev))
tmp_samples, hum_samples = zip(*samples)

final = (sum(tmp_samples)/len(tmp_samples) + config.get('tmp_cal', 0),
         sum(hum_samples)/len(hum_samples) + config.get('hum_cal', 0))

print('* reporting temperature {}, humidity {}'.format(*final))

client = mqtt.MQTTClient(mqtt_id, config['mqtt_server'])
client.connect()
client.publish('sensor/{}/temperature'.format(mqtt_id),
               bytes(str(final[0]), 'utf8'))
client.publish('sensor/{}/humidity'.format(mqtt_id),
               bytes(str(final[1]), 'utf8'))
client.disconnect()

sleep.deepsleep(int(config['interval']))
