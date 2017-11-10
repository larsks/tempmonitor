import machine
from machine import Pin
import network
import select
import socket

ap_if = network.WLAN(network.AP_IF)


class Discover():
    def run(self):
        print('! discovery is not available')
