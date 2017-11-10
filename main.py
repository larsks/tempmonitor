import json

from tempmonitor import discover
from tempmonitor import monitor

try:
    with open('config.json') as fd:
        config = json.load(fd)

    try:
        with open('config_local.json') as fd:
            config.update(json.load(fd))
    except OSError:
        pass

    print('* starting temperature monitor')
    app = monitor.Monitor(config)
except OSError:
    print('! configuration is not available')
    app = discover.Discover()

app.run()
