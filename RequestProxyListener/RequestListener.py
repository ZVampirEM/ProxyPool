import socket
import threading

class Listener(object):
    def __init__(self, listen_addr, listen_port, sf_name):
        self.__m_listen_addr = listen_addr
        self.__m_listen_port = listen_port
        self.socket_server = self.create_socket_server()
        self.__m_thread_list = []
        self.__proxy_save_file = sf_name

    def __del__(self):
        self.socket_server.close()


    def create_socket_server(self):
        my_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # SET ADDRESS REUSE
        my_socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # BIND
        my_socket_server.bind((self.__m_listen_addr, int(self.__m_listen_port)))
        # LISTEN
        my_socket_server.listen(5)

        return my_socket_server

    #listen the request
    def listening_request(self):
        while True:
            sock, addr = self.socket_server.accept()

            print "A New Connect, address = %s:%s" % (addr)

            #create handle thread
            handle_thread = threading.Thread(target=self.handle_client_request, args=(sock, addr))
            handle_thread.start()

            self.__m_thread_list.append(handle_thread)


    def handle_client_request(self, socket_obj, client_addr):
        print "A New Thread to Handle the request for client in address = %s:%s"\
              % (client_addr)

        is_finished = False
        while is_finished == False:
            try:
                recv_request = socket_obj.recv(256)
                print recv_request
            
                if recv_request == 'exit':
                    is_finished = True
                    
            except:
                print "client close"
                break
            
        socket_obj.close()

