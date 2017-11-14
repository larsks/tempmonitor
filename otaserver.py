import board
import errno
import os

from noggin.app import App, HTTPError

app = App()


@app.route('/')
def index(req, match):
    return {
        'sensor_id': board.id(),
        'sensor_type': 'dht',
    }


@app.route('/files/(.*)')
def get_file(req, match):
    path = match.group(1)
    print('* request to get {}'.format(path))
    try:
        with open(path) as fd:
            return fd.read()
    except OSError:
        raise HTTPError(404)


@app.route('/files/(.*)', method='PUT')
def put_file(req, match):
    path = match.group(1)
    print('* request to put {}'.format(path))

    parts = path.split(b'/')
    for i in range(len(parts) - 1):
        partial = b'/'.join(parts[:i + 1])
        print('* create directory {}'.format(partial))
        try:
            os.mkdir(partial)
        except OSError:
            pass

    tmppath = path + b'_otatmp'
    with open(tmppath, 'w') as fd:
        fd.write(req.content)

    os.rename(tmppath, path)


@app.route('/files/(.*)', method='DELETE')
def del_file(req, match):
    path = match.group(1)
    print('* request to delete {}'.format(path))

    try:
        try:
            os.remove(path)
        except OSError as err:
            if err.args[0] == errno.EISDIR:
                os.rmdir(path)
            else:
                raise
    except OSError as err:
        if err.args[0] == errno.ENOENT:
            raise HTTPError(404)
        else:
            raise


@app.route('/reset')
def reset(req, match):
    open('_otareset', 'w').close()
    board.reset()


@app.route('/id')
def get_id(req, match):
    return board.id()


def serve():
    app.serve(port=2112)
