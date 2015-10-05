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
    e = export.AurSirExport(HELLOKEY, '192.168.122.1')
    e.react({"SayHello",greet_back})


def greet_back(r):
    print(r.decode())
    return {"Answer": "Greetings Back from AurSir4py"}

    # iface = interface.Interface()
    # print("OPA")
    #
    # k = appkey.AppKey.fromyaml(HELLOKEY)
    # ia = iface.add_import(k)
    # print(ia.exported)
    # print(ia.id)
    # print(ia.call("SayHello",{"Greeting":"Hello from aursir4py"}).decode())
    #
    #
    #
    #
    # ia.callAll("SayHello",{"Greeting":"Hello from aursir4py"})
    # print(ia.listen().decode())
    # ia.start_listen("SayHello")
    # ia.trigger("SayHello",{"Greeting":"Hello from aursir4py"})
    # print(ia.listen().decode())
    # ia.triggerAll("SayHello",{"Greeting":"Hello from aursir4py"})
    # print(ia.listen().decode())
    # iface.stop()


if __name__ == "__main__":
    main()