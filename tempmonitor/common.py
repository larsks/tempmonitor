try:
    import binascii
except ImportError:
    import ubinascii as binascii

import network


def macaddr():
    sta_if = network.WLAN(network.STA_IF)
    mac = sta_if.config('mac')
    return binascii.hexlify(mac).decode('utf8')
