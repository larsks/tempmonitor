import dht
import machine
from machine import Pin
import time


DEFAULT_DHT_PIN = 4
DEFAULT_LED_PIN = 2


class Board():

    def __init__(self, dht_pin=None, led_pin=None):
        self._dht_pin = dht_pin if dht_pin is not None else DEFAULT_DHT_PIN
        self._led_pin = led_pin if led_pin is not None else DEFAULT_LED_PIN
        self._dht_last_read = time.time()

        self.init_dht()
        self.init_led()

    def init_dht(self):
        print('* temperature sensor on pin {}'.format(self._dht_pin))
        self.dht = dht.DHT22(Pin(self._dht_pin))
        try:
            self._read_dht()
        except OSError:
            pass

    def init_led(self):
        print('* led on pin {}'.format(self._led_pin))
        self.led = Pin(self._led_pin, Pin.OUT)
        self.led.on()

    def led_toggle(self):
        self.led.value(not self.led.value())

    def led_on(self):
        self.led.off()

    def led_off(self):
        self.led.on()

    def deepsleep_ms(self, ms):
        rtc = machine.RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
        rtc.alarm(rtc.ALARM0, ms)

        print('* sleeping for {ms} milliseconds'.format(ms=ms))
        machine.deepsleep()

    def deepsleep(self, s):
        self.deepsleep_ms(s * 1000)

    def reset(self):
        machine.reset()

    def _read_dht(self):
        if (time.time()) - self._dht_last_read > 2:
            time.sleep(2)

        self.dht.measure()
        self._dht_last_read = time.time()

    def read_dht(self):
        while True:
            try:
                self._read_dht()
                tmp, hum = self.dht.temperature(), self.dht.humidity()
                print('# read temperature {}, humidity {}' .format(tmp, hum))
                return {
                    'temperature': tmp,
                    'humidity': hum,
                }
            except OSError:
                print('! failed to read dht22, retrying')
