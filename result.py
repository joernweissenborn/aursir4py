import queue
import time

__author__ = 'joern'

import umsgpack
import libimport


class Result:

    def __init__(self, importer, request):
        self.request = request
        self.importer = importer
        self.q = queue.Queue()
        self.received = False
        self.params = None

    def set_params(self, params):
        self.params = params

    def receive(self, block=True):
        if self.params is not None:
            return True
        data = None
        while data is None:
            data = libimport.GetResult(self.importer, self.request.uuid)
            time.sleep(0.001)
            if not block:
                break
        if data is not None:
            self.params = data
            return True
        return False

    def received(self):
        return self.params is not None

    def decode(self):
        return umsgpack.unpackb(self.params)


