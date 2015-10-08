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
