import socket

class Listener(object):
    def __init__(self, listen_addr, listen_port):
        self.__m_listen_addr = listen_addr
        self.__m_listen_port = listen_port

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # SET ADDRESS REUSE
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #BIND
        self.socket_server.bind((self.__m_listen_addr, int(self.__m_listen_port)))
        #LISTEN
        self.socket_server.listen(5)


    def CreateSocketServer(self):


    def listening_request(self):
        pass