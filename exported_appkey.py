__author__ = 'joern'

import appkey
import uuid
import Queue
import messages


class ExportedAppkey:

    def __init__(self,exportaddedmsg, router):
        self.id = exportaddedmsg["ExportId"]
        self.appkey = appkey.AppKey(exportaddedmsg["AppKey"])
        self.tags = exportaddedmsg["Tags"]

        self.__router = router

        self.__rq = Queue.Queue()
        self.__router.reg_req_q(self.id, self.__rq)

    def request(self):
        return self.__rq.get()

    def reply(self, request, result):
        m = messages.Result.from_request(request, self.id, result)
        self.__router.send(m)