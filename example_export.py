__author__ = 'joern'

import export


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
    e = export.AurSirExport(HELLOKEY, '127.0.0.1')
    e.react(dict([("SayHello", greet_back)]))


def greet_back(r):
    print(r)
    return {"Answer": "Greetings Back from AurSir4py"}


if __name__ == "__main__":
    main()