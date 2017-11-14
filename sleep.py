import machine


def deepsleep_ms(ms):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, ms)

    print('* sleeping for {ms} milliseconds'.format(ms=ms))
    machine.deepsleep()


def deepsleep(s):
    deepsleep_ms(s * 1000)
