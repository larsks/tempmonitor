# Temperature monitor

This is software meant to run on an ESP8266 running [MicroPython][].
It will read temperature and humidity from a DHT22 (or similar) sensor
and deliver it via MQTT to your IoT infrastructure.

---

**WARNING**

This is a work in progress. The software isn't terribly robust and is
still undergoing substantial changes from commit to commit.

**WARNNIG**

---

[micropython]: https://micropython.org/

## Requirements

Before getting started, you will need:

- One or more ESP8266 boards running MicroPython. You can buy these
  for around $3 from [eBay](http://ebay.com).  You will need to
  [install MicroPython][] yourself.

- A corresponding number of DHT22 or similar temperature sensors.

- A way to connect the previous two items.  Soldering, breadboards,
  etc.

- Appropriate cabling. Depending on your ESP8266 board, you may simply
  need a USB cable.  In some cases you may need a USB serial adapter.

- A mechanism for getting files onto your ESP8266, such as
  [ampy][].

[install micropython]: https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html
[ampy]: https://github.com/adafruit/ampy

## Overview

There are two main parts to this repository:

- An "OTA" update service implemented using [Noggin]. When the device
  starts up, it checks a (configurable) URL to see if it should enter
  OTA mode.  If so, it starts up an HTTP server that provides a
  get/put/rename/delete file interface via HTTP.

- The sensor driver itself.  If OTA mode is not requested, the sensor
  will take a reading from the sensor, deliver it via MQTT, and then
  enter deepsleep mode for a configurable length of time.

[noggin]: https://github.com/larsks/micropython-noggin

## Configuration

The code looks for a file named `config.json` on the root of the
filesystem.

    {
      "wifi_ssid": "mynetwork",
      "wifi_password": "secret",
      "mqtt_server": "stats.example.com",
      "ota_check_url": "http://stats.example.com:2112/ota/{id}",
      "interval": 60
    }

The code will optionally read from a file named `config_local.json`
and merge that with the main configuration.
