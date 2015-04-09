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
    ia = iface.add_import(k)
    print(ia.exported)
    print(ia.id)
    print(ia.call("SayHello",{"Greeting":"Hello from aursir4py"}).decode())
    ia.callAll("SayHello",{"Greeting":"Hello from aursir4py"})
    print(ia.listen().decode())
    ia.start_listen("SayHello")
    ia.trigger("SayHello",{"Greeting":"Hello from aursir4py"})
    print(ia.listen().decode())
    iface.stop()


if __name__ == "__main__":
    main()