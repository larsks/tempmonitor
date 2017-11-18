import errno
import gc
import machine
import os

from noggin import Noggin, Response, HTTPError
from noggin.util import chunked_reader

import board

# cribbed from
# https://github.com/micropython/micropython-lib/blob/master/stat/stat.py
S_IFDIR = 0o040000
S_IFMT = 0o170000

app = Noggin()


@app.route('/')
def index(req):
    return {
        'sensor_type': 'dht',
        'sensor_id': board.id()
    }


def get_statvfs():
    statvfs_fields = [
        'bsize',
        'frsize',
        'blocks',
        'bfree',
        'bavail',
        'files',
        'ffree',
    ]
    return dict(zip(statvfs_fields, os.statvfs('/')))


@app.route('/disk/free')
def disk_free(req):
    s = get_statvfs()
    return {
        'blocks': s['bfree'],
        'bytes': (s['bsize'] * s['bfree'])
    }


@app.route('/mem/free')
def mem_free(req):
    return {
        'bytes': gc.mem_free()
    }


def get_file_list(path):
    files = []

    for f in os.listdir(path):
        fp = '/'.join([path, f])
        print('* checking', f)
        s = os.stat(fp)
        if s[0] & S_IFMT == S_IFDIR:
            files.append((f, s[6], True, get_file_list(fp)))
        else:
            files.append((f, s[6], False, None))

    return files


@app.route('/file')
def list_files(req):
    print('* request to list files')
    return get_file_list('/')


@app.route('/file/(.*)')
def get_file(req, path):
    print('* request to get {}'.format(path))
    try:
        with open(path) as fd:
            return chunked_reader(fd)
    except OSError:
        raise HTTPError(404)


@app.route('/file/(.*)', methods=['DELETE'])
def del_file(req, path):
    print('* request to delete {}'.format(path))
    try:
        os.remove(path)
    except OSError as err:
        if err.args[0] == errno.ENOENT:
            raise HTTPError(404)
        else:
            raise HTTPError(500)


@app.route('/file/(.*)', methods=['POST'])
def rename_file(req, path):
    newpath = req.text
    print('* request to rename {} -> {}'.format(path, newpath))
    try:
        os.rename(path, newpath)
    except OSError as err:
        if err.args[0] == errno.ENOENT:
            raise HTTPError(404)
        else:
            raise HTTPError(500)


@app.route('/file/(.*)', methods=['PUT'])
def put_file(req, path):
    print('* request to put {}'.format(path))
    parts = path.split('/')

    for i in range(len(parts) - 1):
        partial = '/'.join(parts[:i + 1])
        print('* create directory {}'.format(partial))
        try:
            os.mkdir(partial)
        except OSError:
            pass

    with open(path, 'w') as fd:
        for chunk in req.iter_content():
            fd.write(chunk)


@app.route('/reset')
def reset(req):
    open('_otareset', 'w').close()
    req.close()
    machine.reset()


def serve():
    app.serve(port=2112)
