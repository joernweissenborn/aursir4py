__author__ = 'joern'

import ctypes

libaursir = ctypes.CDLL('libaursirexport.so')

libaursir.NewExportYAML.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
libaursir.NewExportYAML.restype = ctypes.c_int

libaursir.GetNextRequestId.argtypes = [ctypes.c_int]
libaursir.GetNextRequestId.restype = ctypes.c_char_p


libaursir.RetrieveRequestParams.argtypes = [ctypes.c_int, ctypes.c_char_p]
libaursir.RetrieveRequestParams.restype = ctypes.c_char_p


libaursir.RetrieveRequestFunction.argtypes = [ctypes.c_int, ctypes.c_char_p]
libaursir.RetrieveRequestFunction.restype = ctypes.c_char_p

libaursir.Reply.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
libaursir.Reply.restype = ctypes.c_int


libaursir.Emit.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
libaursir.Emit.restype = ctypes.c_int

