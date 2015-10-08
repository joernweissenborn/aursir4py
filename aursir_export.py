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
# along with aursir4py.  If not, see <http://www.gnu.org/licenses/>.__author__ = 'Joern Weissenborn'

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
