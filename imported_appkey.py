__author__ = 'joern'

import appkey
import uuid
import Queue
import messages

class ImportedAppkey:
    def __init__(self,importaddedmsg, router):
        self.id = importaddedmsg["ImportId"]
        self.appkey = appkey.AppKey(importaddedmsg["AppKey"])
        self.tags = importaddedmsg["Tags"]
        self.exported = importaddedmsg["Exported"]

        self.__router = router

        self.__listenq = Queue.Queue()
        self.__router.reg_listen_q(self.id, self.__listenq)

    def call(self, functionname, parameter):
        Uuid = uuid.uuid4().hex

        rq = Queue.Queue()
        self.__router.reg_res_q(Uuid,rq)
        self.__call(Uuid,functionname,parameter,0)
        return rq.get()

    def trigger(self, functionname, parameter):
        Uuid = uuid.uuid4().hex

        self.__call(Uuid,functionname,parameter,1)
        return

    def callAll(self, functionname, parameter):
        Uuid = uuid.uuid4().hex

        self.__call(Uuid,functionname,parameter,2)
        return

    def triggerAll(self, functionname, parameter):
        Uuid = uuid.uuid4().hex

        self.__call(Uuid,functionname,parameter,3)
        return

    def __call(self, Uuid, functionname, parameter, calltype):
        m = messages.Request.from_parameter(self.appkey.ApplicationKeyName,functionname,calltype,self.tags, Uuid, self.id,parameter)
        self.__router.send(m)
        return

    def listen(self):
        return self.__listenq.get()

    def start_listen(self, functionname):
        m = messages.ListenMessage(self.id, functionname)
        self.__router.send(m)
    def stop_listen(self, functionname):
        m = messages.StopListenMessage(self.id, functionname)
        self.__router.send(m)