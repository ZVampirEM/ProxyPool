from ThreadBase import ThreadBaseModule
import RequestListener

class RequestListenerThread(ThreadBaseModule.OriginalThread):
    def __init__(self):
        self.request_listener = RequestListener.Listener()
        ThreadBaseModule.OriginalThread.__init__(self)

    def Initialize(self):
        self.request_listener.create_socket_server()
        return True

    def Run(self):
        self.request_listener.listening_request()

    def ExitInstance(self):
        del self.request_listener

    def Stop(self):
        # close the listener socket and worker socket
        pass
