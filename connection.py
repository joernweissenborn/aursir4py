__author__ = 'joern'

import zmq
import threading
import socket
import Queue
import messages
import json
import time
import imported_appkey
import exported_appkey

class Outgoing(threading.Thread):
    def __init__(self,uuid, ctx, port, q, stopevt):
        threading.Thread.__init__(self)
        self.q = q
        self.port = port
        self.skt = ctx.socket(zmq.DEALER)
        self.skt.identity = uuid
        self.skt.connect("tcp://localhost:5555")


        self.__udpping = UdpPing(port,uuid,stopevt)
        self.__udpping.start()

        self.stopevt = stopevt

    def __send(self, msg):
        payload = ["%d" % msg.getType(),"JSON",msg.encode(),"%d" % self.port]
        self.skt.send_multipart(payload)

    def run(self):
        while not self.stopevt.is_set():
            try:
                msg = self.q.get(False, 1000)
            except:
                pass
            else:
                self.__send(msg)
        self.__send(messages.LeaveMessage())

class Incoming(threading.Thread):
    def __init__(self, ctx,q, stopevt):
        threading.Thread.__init__(self)
        self.q = q
        self.stopevt = stopevt
        self.skt = ctx.socket(zmq.ROUTER)
        self.port = self.skt.bind_to_random_port("tcp://127.0.0.1")
        self.skt.RCVTIMEO = 1000

    def run(self):
        while not self.stopevt.is_set():
            try:
                m = self.skt.recv_multipart()
            except:
                pass
            else:
                self.q.put(m)


class Router(threading.Thread):



    def __init__(self,Uuid):
        threading.Thread.__init__(self)
        self.__inq = Queue.Queue()
        self.__outq = Queue.Queue()

        self.dockedq = Queue.Queue()

        ctx = zmq.Context()

        self.stopevt = threading.Event()


        self.__i = Incoming(ctx,self.__inq, self.stopevt)
        self.__i.start()

        self.__o = Outgoing(Uuid, ctx, self.__i.port, self.__outq,self.stopevt)
        self.__o.start()

        self.__resqs = {}
        self.__reqqs = {}
        self.__listenqs = {}
        self.__impaddedqs = {}
        self.__expaddedqs = {}

        self.switch = {
            messages.Types.DOCKED: self.docked,
            messages.Types.IMPORT_ADDED: self.import_added,
            messages.Types.EXPORT_ADDED: self.export_added,
            messages.Types.RESULT: self.result,
            messages.Types.REQUEST: self.request,

            }

    def send(self,message):
        self.__outq.put(message)


    def stop(self):
        self.stopevt.set()

    def reg_import_added_q(self,ik,q):
        self.__impaddedqs[ik] = q

    def reg_export_added_q(self,ek,q):
        self.__expaddedqs[ek] = q

    def reg_res_q(self,Uuid,q):
        self.__resqs[Uuid] = q
    def reg_req_q(self,Expid,q):
        self.__reqqs[Expid] = q

    def reg_listen_q(self,importid,q):
        self.__listenqs[importid] = q

    def run(self):
        while not self.stopevt.is_set():
            try:
                m = self.__inq.get(False, 1000)
            except:
                pass
            else:
                t = int(m[1])
                if t in self.switch:
                    self.switch[t](m[3])
                else:
                    print("Unknown msg")


    def docked(self,m):
        self.dockedq.put(json.loads(m)['Ok'])

    def import_added(self,m):
        ia = imported_appkey.ImportedAppkey(json.loads(m), self)
        ikey = ia.appkey.ApplicationKeyName
        for t in ia.tags:
            ikey += t
        self.__impaddedqs[ikey].put(ia)
        del self.__impaddedqs[ikey]

    def export_added(self,m):
        ea = exported_appkey.ExportedAppkey(json.loads(m), self)
        ekey = ea.appkey.ApplicationKeyName
        for t in ea.tags:
            ekey += t
        self.__expaddedqs[ekey].put(ea)
        del self.__expaddedqs[ekey]

    def result(self,m):
        r = messages.Result.from_message(json.loads(m))
        if r.CallType == 0:
            self.__resqs[r.Uuid].put(r)
        else:
            self.__listenqs[r.ImportId].put(r)

    def request(self,m):
        r = messages.Request.from_message(json.loads(m))
        self.__reqqs[r.ExportId].put(r)

class UdpPing(threading.Thread):
    def __init__(self, port, Uuid, stopevt):
        threading.Thread.__init__(self)
        self.stopevt = stopevt
        self.port = port
        self.uuid = Uuid
        self.skt = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def run(self):
        print("pingstart")
        print(self.stopevt.is_set())
        while not self.stopevt.is_set():
            self.skt.sendto(self.uuid, ("127.0.0.1", 5557))
            time.sleep(1)
