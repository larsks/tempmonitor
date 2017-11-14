import board
import json
import machine
import os
import time
import urequests as requests


class TimeoutError(Exception):
    pass

config = {
    'ap_wifi_ssid': 'sensor-{}'.format(board.id()),
    'ap_wifi_password': 'sensornet',
    'wifi_connection_timeout': 30,
}


def load_config():
    global config

    try:
        with open('config.json') as fd:
            config.update(json.load(fd))

        try:
            with open('config_local.json') as fd:
                config.update(json.load(fd))
        except OSError:
            pass
    except OSError:
        pass


def stop_ap():
    global config

    print('* stopping access point')
    board.ap_if.active(False)
    while board.ap_if.active():
        machine.idle


def start_ap():
    global config

    print('* starting access point')
    board.ap_if.active(True)
    while not board.ap_if.active():
        machine.idle
    board.ap_if.config(essid=config['ap_wifi_ssid'])
    board.ap_if.config(password=config['ap_wifi_password'])


def wait_for_connection():
    global config

    print('* waiting for wifi')
    time_start = time.time()
    while not board.sta_if.isconnected():
        time.sleep(1)
        time_now = time.time()
        if time_now - time_start > config['wifi_connection_timeout']:
            raise TimeoutError()


def start_network():
    global config
    global hard_reset
    global ota_reset
    global have_net_config
    global want_ota_mode

    if ((not board.sta_if.active() and have_net_config) or
            (hard_reset and have_net_config) or
            (ota_reset and have_net_config)):
        print('* connecting to network {wifi_ssid}'.format(**config))
        board.sta_if.active(True)
        while not board.sta_if.active():
            machine.idle()

        board.sta_if.connect(config['wifi_ssid'], config.get('wifi_password'))
    elif board.sta_if.active() and not have_net_config:
        print('* network configuration is stale')
        board.sta_if.active(False)
        while board.sta_if.active():
            machine.idle()
    else:
        print('* using existing network configuration')

    if not board.sta_if.active():
        start_ap()
        want_ota_mode = True
    else:
        try:
            wait_for_connection()
            stop_ap()
            print('* connected as {}'.format(board.sta_if.ifconfig()))
        except TimeoutError:
            print('! failed to connect to network')
            start_ap()
            want_ota_mode = True

load_config()

want_ota_mode = False
hard_reset = machine.reset_cause() == machine.HARD_RESET
have_net_config = 'wifi_ssid' in config

try:
    os.remove('_otareset')
    ota_reset = True
except OSError:
    ota_reset = False

start_network()

ota_check_url = config.get('ota_check_url')
if not want_ota_mode and ota_check_url:
    try:
        res = requests.get(ota_check_url.format(id=board.id()))
        want_ota_mode = res.json().get('ota_mode', False)
    except (ValueError, OSError) as err:
        print('! failed to check ota endpoint: {}'.format(err))


if want_ota_mode:
    print('* starting ota mode')
    import otaserver
    otaserver.serve()
else:
    print('* starting main app')
    import main_stage2
