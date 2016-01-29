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


