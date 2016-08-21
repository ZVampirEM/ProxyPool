import threading

_SaveFile_ThreadLock = threading.Lock()
_VariFile_ThreadLock = threading.Lock()

def SaveFileLock():
    _SaveFile_ThreadLock.acquire()

def SaveFileUnLock():
    _SaveFile_ThreadLock.release()

def VariFileLock():
    _VariFile_ThreadLock.acquire()

def VariFileUnLock():
    _VariFile_ThreadLock.release()