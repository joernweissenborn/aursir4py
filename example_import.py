import time

__author__ = 'joern'

from aursir_import import AurSirImport

HELLOKEY = '''
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
    i = AurSirImport(HELLOKEY, '127.0.0.1')

    time.sleep(1)

    res = i.call('SayHello', dict([('Greeting', 'Hello From AurSir4pi')]))

    res.receive()

    print(res.decode())

if __name__ == "__main__":
    main()
