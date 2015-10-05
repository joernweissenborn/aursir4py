__author__ = 'joern'

import ctypes

libaursirexport = ctypes.CDLL('libaursirexport.so')

NewExportYaml = libaursirexport.NewExportYAML
NewExportYaml.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
NewExportYaml.restype = ctypes.c_int

GetNextRequestId = libaursirexport.GetNextRequestId
GetNextRequestId.argtypes = [ctypes.c_int]
GetNextRequestId.restype = ctypes.c_char_p


RetrieveRequestParams = libaursirexport.RetrieveRequestParams
RetrieveRequestParams.argtypes = [ctypes.c_int, ctypes.c_char_p]
RetrieveRequestParams.restype = ctypes.c_char_p


RetrieveRequestFunction = libaursirexport.RetrieveRequestFunction
RetrieveRequestFunction.argtypes = [ctypes.c_int, ctypes.c_char_p]
RetrieveRequestFunction.restype = ctypes.c_char_p

Reply = libaursirexport.Reply
Reply.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
Reply.restype = ctypes.c_int


Emit = libaursirexport.Emit
Emit.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
Emit.restype = ctypes.c_int

