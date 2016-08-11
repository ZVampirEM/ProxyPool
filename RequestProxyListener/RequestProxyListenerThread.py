from ThreadBase import ThreadBaseModule
import RequestListener

class RequestListenerThread(ThreadBaseModule.OriginalThread):
    def __init__(self, addr, port, savefile_name):
        ThreadBaseModule.OriginalThread.__init__(self)
        self.request_listener = RequestListener.Listener(addr, port, savefile_name)

    def Initialize(self):
        return True

    def Run(self):
        self.request_listener.listening_request()

    def ExitInstance(self):
        del self.request_listener

    def Stop(self):
        # close the listener socket and worker socket
        pass
