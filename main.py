import json

from tempmonitor import discover
from tempmonitor import monitor

try:
    with open('config.json') as fd:
        config = json.load(fd)

    print('* starting temperature monitor')
    app = monitor.Monitor(config)
except OSError:
    print('! configuration is not available')
    app = discover.Discover()

app.run()
