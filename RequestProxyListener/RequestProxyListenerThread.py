from ThreadBase import ThreadBaseModule
import RequestListener

class RequestListenerThread(ThreadBaseModule.OriginalThread):
    def __init__(self, addr, port):
        ThreadBaseModule.OriginalThread.__init__()
        self.request_listener = RequestListener.Listener(addr, port)

    def Initialize(self):
        return True

    def Run(self):
        self.request_listener.listening_request()

    def ExitInstance(self):
        del self.request_listener
