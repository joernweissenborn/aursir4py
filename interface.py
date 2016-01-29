__author__ = 'joern'

import uuid
import connection
import Queue
import messages


class Interface():

    def __init__(self, appname="PythonApp"):
        self.appname = appname
        self.uuid = uuid.uuid4().hex
        self.__router = connection.Router(self.uuid)
        self.__router.start()
        self.__dock()

    def stop(self):
        print("STOPPING")
        self.__router.stop()


    def __dock(self):
        m = messages.DockMessage(self.appname)
        self.__router.send(m)
        if self.__router.dockedq.get():
            print("Docksuccess")
        else:
            print("Dockfail")

    def add_import(self,appkey, tags=[]):
        m = messages.AddImportMessage(appkey,tags)
        impkey = appkey.ApplicationKeyName
        for t in tags:
            impkey += t
        q = Queue.Queue()
        self.__router.reg_import_added_q(impkey,q)
        self.__router.send(m)
        return q.get()

    def add_export(self,appkey, tags=[]):
        m = messages.AddExportMessage(appkey,tags)
        expkey = appkey.ApplicationKeyName
        for t in tags:
            expkey += t
        q = Queue.Queue()
        self.__router.reg_export_added_q(expkey,q)
        self.__router.send(m)
        return q.get()