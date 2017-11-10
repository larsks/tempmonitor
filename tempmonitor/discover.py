import machine
from machine import Pin
import network
import select
import socket
import time

from tempmonitor.common import macaddr

ap_if = network.WLAN(network.AP_IF)


class Discover():
    def __init__(self,
                 wifi_prefix='sensor',
                 wifi_password='sensornet'):

        self.wifi_prefix = wifi_prefix
        self.wifi_password = wifi_password
        self.led = Pin(2, Pin.OUT)
        self.macaddr = macaddr()

    def run(self):
        self.configure_network()
        self.configure_sockets()

    def create_socket(self):
        self.sock = socket.socket()
        self.sock.bind(('', self.prot))
        self.sock.listen(1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.poll = select.poll()
        self.poll.register(self.sock, select.POLLIN|select.POLLHUP)

    def configure_network(self):
        ssid = '{}-{}'.format(self.wifi_prefix, self.macaddr)
        print('* configuring network {}'.format(ssid))

        if not ap_if.active():
            ap_if.active(True)

            while not ap_if.active():
                machine.idle()

        ap_if.config(essid=ssid,
                     authmode=network.AUTH_WPA_WPA2_PSK,
                     password=self.wifi_password)
