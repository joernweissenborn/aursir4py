__author__ = 'Joern Weissenborn'

import queue
import threading
import time
import umsgpack
import libimport
from request import Request
from result import Result


class AurSirImport:
    def __init__(self, service_descriptor, address):

        self.id = libimport.NewImportYAML(service_descriptor.encode('ascii'), address.encode('ascii'))
        self.listen_q = queue.Queue()
        self.listen_receiver = ListenReceiver(self.id, self.listen_q)
        self.listen_receiver.start()

    def call(self, function, parameter):
        uuid = libimport.Call(self.id, function.encode("ascii"), umsgpack.packb(parameter))
        return Result(self.id, Request(uuid, function, parameter, None))

    def trigger(self, function, parameter):
        libimport.Trigger(self.id, function.encode("ascii"), umsgpack.packb(parameter))

    def trigger_all(self, function, parameter):
        libimport.TriggerAll(self.id, function.encode("ascii"), umsgpack.packb(parameter))

    def listen(self, function):
        libimport.Listen(self.id, function.encode("ascii"))

    def stop_listen(self, function):
        libimport.StopListen(self.id, function.encode("ascii"))



class ListenReceiver(threading.Thread):
    def __init__(self, iid, listen_q):
        super(ListenReceiver, self).__init__()
        self.iid = iid
        self.listen_q = listen_q

    def run(self):
        while True:
            rid = libimport.GetNextListenResult(self.iid)
            if rid is not None:
                function = libimport.GetNextListenResultFunction(self.iid)
                inparams = libimport.GetNextListenResultInParameter(self.iid)
                params = libimport.GetNextListenResultParameter(self.iid)
                request = Request(rid, function, inparams, None)
                result = Result(self.iid, request)
                result.set_params(params)
                self.listen_q.put(result)
            time.sleep(0.01)
