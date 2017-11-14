try:
    import binascii
except ImportError:
    import ubinascii as binascii

import machine
import network

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)


def id():
    sta_if = network.WLAN(network.STA_IF)
    mac = sta_if.config('mac')
    return binascii.hexlify(mac).decode('utf8')


def deepsleep_ms(ms):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, ms)

    print('* sleeping for {ms} milliseconds'.format(ms=ms))
    machine.deepsleep()


def deepsleep(s):
    deepsleep_ms(s * 1000)


def reset():
    machine.reset()
