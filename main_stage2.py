from tempmonitor.monitor import Monitor


def main(config):
    m = Monitor(config)
    m.run()
