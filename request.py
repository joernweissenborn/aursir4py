__author__ = 'joern'

import umsgpack
import libexport


class Request:
    def __init__(self, uuid, function, params, exporter):
        self.uuid = uuid
        self.function = function
        self.params = params
        self.exporter = exporter

    def decode(self):
        return umsgpack.unpackb(self.params)

    def reply(self, params):
        if self.exporter is None:
            return
        libexport.Reply(self.exporter, self.uuid, umsgpack.packb(params))
