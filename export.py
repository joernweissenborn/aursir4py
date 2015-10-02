import queue
import threading
import time
import umsgpack

from request import Request
__author__ = 'Joern Weissenborn'

from lib import libaursir


class AurSirExport:
    def __init__(self, service_descriptor, address):

        self.id = libaursir.NewExportYAML(service_descriptor.encode('ascii'), address.encode('ascii'))
        self.idq = queue.Queue()
        self.receiver = ExportReceiver(self.id, self.idq)
        self.receiver.start()

    def request(self):
        uuid = self.idq.get()
        print(uuid)
        function = libaursir.RetrieveRequestFunction(self.id, uuid)
        params = libaursir.RetrieveRequestParams(self.id, uuid)
        return Request(uuid, function, params, self.id)

    def emit(self, inparams, outparams):
        libaursir.Emit(self.id, umsgpack.packb(inparams), umsgpack.packb(outparams))

class ExportReceiver(threading.Thread):
    def __init__(self, eid, idq):
        super(ExportReceiver, self).__init__()
        self.eid = eid
        self.idq = idq

    def run(self):
        while True:
            rid = libaursir.GetNextRequestId(self.eid)
            if rid is not None:
                self.idq.put(rid)
            time.sleep(0.001)
