# Copyright (c) 2015 Joern Weissenborn
#
# This file is part of aursir4py.
#
# aursir4py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# aursir4py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with aursir4py.  If not, see <http://www.gnu.org/licenses/>.

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

    def get_listen_result(self, block=True):
        return self.listen_q.get(block=block)


class ListenReceiver(threading.Thread):
    def __init__(self, iid, listen_q):
        super(ListenReceiver, self).__init__()
        self.iid = iid
        self.listen_q = listen_q

    def run(self):
        while True:
            rid = libimport.GetNextListenResult(self.iid)
            if rid is not None:
                function = libimport.GetNextListenResultFunction(self.iid).decode('ascii')
                inparams = libimport.GetNextListenResultInParameter(self.iid)
                params = libimport.GetNextListenResultParameter(self.iid)
                request = Request(rid, function, inparams, None)
                result = Result(self.iid, request)
                result.set_params(params)
                self.listen_q.put(result)
            time.sleep(0.001)
