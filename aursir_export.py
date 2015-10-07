import queue
import threading
import time
import umsgpack

from request import Request
__author__ = 'Joern Weissenborn'

import libexport


class AurSirExport:
    def __init__(self, service_descriptor, address):

        self.id = libexport.NewExportYaml(service_descriptor.encode('ascii'), address.encode('ascii'))
        self.idq = queue.Queue()
        self.receiver = ExportReceiver(self.id, self.idq)
        self.receiver.start()

    def request(self):
        uuid = self.idq.get()
        print(uuid)
        function = libexport.RetrieveRequestFunction(self.id, uuid).decode("ascii")
        params = libexport.RetrieveRequestParams(self.id, uuid)
        return Request(uuid, function, params, self.id)

    def emit(self, inparams, outparams):
        libexport.Emit(self.id, umsgpack.packb(inparams), umsgpack.packb(outparams))

    def react(self, reactions):
        while True:
            req = self.request()
            reaction = reactions[req.function]
            req.reply(reaction(req.decode()))

class ExportReceiver(threading.Thread):
    def __init__(self, eid, idq):
        super(ExportReceiver, self).__init__()
        self.eid = eid
        self.idq = idq

    def run(self):
        while True:
            rid = libexport.GetNextRequestId(self.eid)
            if rid is not None:
                self.idq.put(rid)
            time.sleep(0.001)
