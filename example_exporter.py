__author__ = 'joern'

import interface
import appkey

HELLOKEY = '''
applicationkeyname: org.aursir.helloaursir

functions:
  - name: SayHello
    input:
      - name: Greeting
        type: 1
    output:
      - name: Answer
        type: 1
   '''

def main():

    iface = interface.Interface()
    print("OPA")

    k = appkey.AppKey.fromyaml(HELLOKEY)
    ea = iface.add_export(k)
    print(ea.id)
    while True:
        r = ea.request()
        print(r.decode())
        ea.reply(r,{"Answer": "Greetings back from aursir4py, you said "+r.decode()["Greeting"]})


if __name__ == "__main__":
    main()