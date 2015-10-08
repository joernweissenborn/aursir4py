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

from aursir_import import AurSirImport

# HELLO_SERVICE describes a simple service which can be greeted and greets back
HELLO_SERVICE = '''
functions:
  - name: SayHello
    input:
      - name: Greeting
        type: string
    output:
      - name: Answer
        type: string
'''


def main():

    # create the AurSir Import with the HELLO_SERVICE service descriptor and bind it to localhost
    i = AurSirImport(HELLO_SERVICE, '127.0.0.1')

    # call works like request reply
    res = i.call('SayHello', dict([('Greeting', 'Hello From AurSir4pi')]))

    # wait for a reply
    res.receive()

    # get the data
    print(res.decode())

if __name__ == "__main__":
    main()
