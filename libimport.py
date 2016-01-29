__author__ = 'joern'

import ctypes

libaursirimport = ctypes.CDLL('libaursirimport.so')

NewImportYAML = libaursirimport.NewImportYAML
NewImportYAML.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
NewImportYAML.restype = ctypes.c_int

Listen = libaursirimport.Listen
Listen.argtypes = [ctypes.c_int, ctypes.c_char_p]

StopListen = libaursirimport.StopListen
StopListen.argtypes = [ctypes.c_int, ctypes.c_char_p]

Call = libaursirimport.Call
Call.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
Call.restype = ctypes.c_char_p

CallAll = libaursirimport.CallAll
CallAll.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
CallAll.restype = ctypes.c_char_p

Trigger = libaursirimport.Trigger
Trigger.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]

TriggerAll = libaursirimport.TriggerAll
TriggerAll.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]

GetResult = libaursirimport.GetResult
GetResult.argtypes = [ctypes.c_int, ctypes.c_char_p]
GetResult.restype = ctypes.c_char_p

GetNextListenResult = libaursirimport.GetNextListenResult
GetNextListenResult.argtypes = [ctypes.c_int]
GetNextListenResult.restype = ctypes.c_char_p

GetNextListenResultFunction = libaursirimport.GetNextListenResultFunction
GetNextListenResultFunction.argtypes = [ctypes.c_int]
GetNextListenResultFunction.restype = ctypes.c_char_p

GetNextListenResultInParameter = libaursirimport.GetNextListenResultInParameter
GetNextListenResultInParameter.argtypes = [ctypes.c_int]
GetNextListenResultInParameter.restype = ctypes.c_char_p

GetNextListenResultParameter = libaursirimport.GetNextListenResultParameter
GetNextListenResultParameter.argtypes = [ctypes.c_int]
GetNextListenResultParameter.restype = ctypes.c_char_p

