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

import export


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
    # create and AurSirExport
    e = export.AurSirExport(HELLO_SERVICE, '127.0.0.1')

    # run the reactor with a dict FunctionName -> Callback
    e.react(dict([("SayHello", greet_back)]))


def greet_back(result):

    print(result)

    # return a dict with the parameters
    return {"Answer": "Greetings Back from AurSir4py"}


if __name__ == "__main__":
    main()