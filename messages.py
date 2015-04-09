__author__ = 'joern'

import base64
import json
from abc import ABCMeta, abstractmethod

class Types():
    DOCK = 0
    DOCKED          = 1
    LEAVE           = 2
    REQUEST         = 3
    RESULT          = 4
    ADD_EXPORT      = 5
    UPDATE_EXPORT   = 6
    EXPORT_ADDED    = 7
    ADD_IMPORT      = 8
    UPDATE_IMPORT   = 9
    IMPORT_ADDED    = 10
    IMPORT_UPDATED  = 11
    LISTEN          = 12
    STOP_LISTEN     = 13
    REMOVE_EXPORT   = 14
    REMOVE_IMPORT   = 15

class MsgEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class Message:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getType(self):
        pass

    def encode(self):
        return json.dumps(self,cls=MsgEncoder)

class DockMessage(Message):
    def __init__(self, appname):
        self.AppName = appname
        self.Codecs = ['JSON']
        self.Node = False

    def getType(self):
        return Types.DOCK

class LeaveMessage(Message):

    def getType(self):
        return Types.LEAVE

class AddImportMessage(Message):
    def __init__(self, appkey, tags):
        self.AppKey = appkey
        self.Tags = tags

    def getType(self):
        return Types.ADD_IMPORT


class Request(Message):
    def __init__(self, appkeyname, functionname, calltype, tags, uuid, importid, exportid, codec, result):
        self.AppKeyName = appkeyname
        self.FunctionName = functionname
        self.CallType = calltype
        self.Tags = tags
        self.Uuid = uuid
        self.ImportId  = importid
        self.ExportId  = exportid
        self.Codec = codec
        self.Result = result
        self.Stream	= False
        self.StreamFinished = True

    @classmethod
    def from_parameter(cls, appkeyname, functionname, calltype, tags, uuid, importid, result):
        return cls(appkeyname,
                   functionname,
                   calltype,
                   tags,
                   uuid,
                   importid,
                   "",
                   "JSON",
                   base64.b64encode(json.dumps(result))
        )

    @classmethod
    def from_message(cls, m):
        return cls(m["AppKeyName"],
                   m["FunctionName"],
                   m["CallType"],
                   m["Tags"],
                   m["Uuid"],
                   m["ImportId"],
                   m["ExportId"],
                   m["Codec"],
                   m["Request"],
                   )

    def getType(self):
        return Types.REQUEST


class Result(Message):
    def __init__(self, appkeyname, functionname, calltype, tags, uuid, importid, exportid, codec, result):
        self.AppKeyName = appkeyname
        self.FunctionName = functionname
        self.CallType = calltype
        self.Tags = tags
        self.Uuid = uuid
        self.ImportId  = importid
        self.ExportId  = exportid
        self.Codec = codec
        self.Result = result
        self.Stream	= False
        self.StreamFinished = True

    @classmethod
    def from_request(cls, request, exportid, result):
        return cls(request.AppKeyName,
                   request.FunctionName,
                   request.CallType,
                   request.Tags,
                   request.Uuid,
                   request.ImportId,
                   exportid,
                   "JSON",
                   base64.b64encode(json.dumps(result))
        )

    @classmethod
    def from_message(cls, resultmsg):
        return cls(resultmsg["AppKeyName"],
                   resultmsg["FunctionName"],
                   resultmsg["CallType"],
                   resultmsg["Tags"],
                   resultmsg["Uuid"],
                   resultmsg["ImportId"],
                   resultmsg["ExportId"],
                   resultmsg["Codec"],
                   resultmsg["Result"],
                   )

    def getType(self):
        return Types.RESULT

    def decode(self):
        return json.loads(base64.b64decode(self.Result))