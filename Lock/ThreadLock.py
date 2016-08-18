import threading

_ThreadLock = threading.Lock()

def Lock():
    _ThreadLock.acquire()

def UnLock():
    _ThreadLock.release()