from omnitools import FTPESS, FTPS
from collections import deque
import threading
import time
import os


class FTPRelayFO:
    def __init__(self, length: int = 0, buf_size: int = 8192, ignore_seek: bool = False):
        self.buf_size = buf_size
        self.buffer = deque()
        self.name = None
        self.closed = False
        self.timeout = 5
        self.parts = 0
        self.length = length
        self.has_length = not not length
        self.red = 0
        self.ignore_seek = ignore_seek

    def __repr__(self):
        return "<{}.{}(length={}) name={} buffer={} parts={} red={} closed={} at {}>".format(
            __name__,
            self.__class__.__name__,
            self.length,
            self.name,
            "deque[memoryview]...{}".format(len(self.buffer)),
            self.parts,
            self.red,
            self.closed,
            hex(id(self))
        )

    def __str__(self):
        return repr(self)

    def tell(self):
        return self.red

    def __len__(self):
        return self.length

    def __iter__(self):
        yield self.read(self.buf_size)

    def seek(self, offset: int, whence: int = 0):
        if whence == 1:
            if offset < 0:
                offset = 0
            self.read(offset)
        elif whence == 2:
            if offset == 0:
                self.close()
                self.buffer.clear()
                self.red = self.length
                return self.red
            offset = self.length - self.red - offset
            if offset <= 0:
                offset = self.length - self.red
            return self.seek(offset, 1)
        else:
            if not self.ignore_seek:
                raise NotImplementedError
            else:
                return offset
        return self.red

    def _read(self):
        start = time.time()
        while True:
            try:
                return self.buffer.pop()
            except IndexError:
                if self.closed or time.time()-start > self.timeout:
                    return memoryview(b"")
            except Exception as e:
                print(e)

    def read(self, n: int = -1, do_red=True):
        if n < 0:
            try:
                return b"".join(_.tobytes() for _ in self.buffer)
            finally:
                self.red = self.length
        if n == 0:
            return b""
        red = self._read()
        l = len(red)
        if l == 0:
            return red.tobytes()
        if l == n:
            if do_red:
                self.red += n
            return red.tobytes()
        elif l > n:
            self.buffer.append(red[n:])
            if do_red:
                self.red += n
            return red[:n].tobytes()
        else:
            red = bytearray(red.tobytes())
            if do_red:
                self.red += l
            while l < n:
                _red = self._read()
                _l = len(_red)
                if l+_l > n:
                    _l = n-l
                    self.buffer.append(_red[_l:])
                    _red = _red[:_l].tobytes()
                l += _l
                red.extend(_red)
                if do_red:
                    self.red += _l
                if not _red:
                    return bytes(red)
            return bytes(red)

    def write(self, s: bytes):
        _ = len(s)
        self.buffer.appendleft(memoryview(s))
        self.parts += 1
        if not self.has_length:
            self.length += _
        return _

    def fileno(self):
        raise AttributeError("do not use sendfile()")

    def close(self):
        self.closed = True

    def flush(self):
        pass


def fake_remote_server_setup(server_type, credentials):
    if not credentials:
        credentials = ["foxe6"]*2
    port = 8022
    users = credentials+["elradfmwMT"]
    remote_homebase = os.path.abspath(r"s2")
    s2 = server_type(port=port)
    s2.server.max_cons = 10
    s2.server.max_cons_per_ip = 10
    homedir = os.path.join(remote_homebase, users[0])
    os.makedirs(homedir, exist_ok=True)
    s2.handler.authorizer.add_user(*users[:2], homedir, users[-1])
    if issubclass(server_type, FTPESS):
        s2.handler.certfile = os.path.join(remote_homebase, "foxe2.pem")
        s2.handler.tls_control_required = True
        s2.handler.tls_data_required = True
    s2.handler.passive_ports = range(51200, 52200)
    s2.configure()
    p2 = threading.Thread(target=s2.start)
    p2.daemon = True
    p2.start()
    return ["127.0.0.1", port], credentials


def fake_ftpes_remote_server_setup(credentials: list = None):
    return fake_remote_server_setup(FTPESS, credentials)


def fake_ftps_remote_server_setup(credentials: list = None):
    return fake_remote_server_setup(FTPS, credentials)


