__author__ = 'joern'

import umsgpack
from lib import libaursir

class Request:
    def __init__(self, uuid, function, params, exporter):
        self.uuid = uuid
        self.function = function
        self.params = params
        self.exporter = exporter

    def decode(self):
        print(type(self.params))
        return umsgpack.unpackb(self.params)

    def reply(self, params):
        libaursir.Reply(self.exporter, self.uuid, umsgpack.packb(params))
        # libaursir.Reply(self.exporter, self.uuid, umsgpack.packb(params))