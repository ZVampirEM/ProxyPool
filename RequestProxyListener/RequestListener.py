import socket
import threading
import re
from Lock import ThreadLock
from conf import ProxyPoolConfig


class Listener(object):
    def __init__(self):
        self.__m_listen_addr = ProxyPoolConfig.config_instance.get_listen_addr
        self.__m_listen_port = ProxyPoolConfig.config_instance.get_listen_port
        self.socket_server = None
        self.__m_send_proxy_list = []
        self.__proxy_vari_file = ProxyPoolConfig.config_instance.get_varifile_name
        self.request_num_pattern = re.compile(r'R_(\d+)')

    def __del__(self):
        self.socket_server.close()


    def create_socket_server(self):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # SET ADDRESS REUSE
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # BIND
        self.socket_server.bind((self.__m_listen_addr, int(self.__m_listen_port)))
        # LISTEN
        self.socket_server.listen(5)

#        return my_socket_server

    #listen the request
    def listening_request(self):
        while True:
            sock, addr = self.socket_server.accept()

            print "A New Connect, address = %s:%s" % (addr)

            #create handle thread
            handle_thread = threading.Thread(target=self.handle_client_request, args=(sock, addr))
            handle_thread.start()


    def handle_client_request(self, socket_obj, client_addr):
        print "A New Thread to Handle the request for client in address = %s:%s"\
              % (client_addr)

        is_finished = False
        while is_finished == False:
            recv_request = socket_obj.recv(4)
            print recv_request

            match_obj = self.request_num_pattern.match(recv_request)

            if match_obj:
                request_proxy_num = int(match_obj.group(1))
                self.__m_send_proxy_list = self.GetProxy(request_proxy_num)
                socket_obj.send(",".join(self.__m_send_proxy_list))


            elif recv_request == 'exit' or not recv_request:
                is_finished = True

            else:
                continue

        socket_obj.close()
        print "close the connect"
    
    def FilterProxy(self, proxy):
        proxy_under_test = dict(http = proxy[:-1])
        print proxy_under_test
        try:
            rtn_obj = self.__m_filter_session.get(self.__m_filter_url, headers = self.__m_headers, proxies = proxy_under_test, timeout = 5)
            print rtn_obj.status_code
            print rtn_obj.ok
            if rtn_obj.ok:
                print "proxy {0} work!".format(proxy[:-1])
                return True
            else:
                print "proxy {0} can't work".format(proxy[:-1])
                return False
        except:
#            print rtn_obj.status
            print "proxy {0} can't work".format(proxy[:-1])
            return False
            

    def GetProxy(self, request_num):
        proxy_list = []
        ThreadLock.VariFileLock()
        try:
            proxy_pool_fp = open(self.__proxy_vari_file, 'r')
        except:
            proxy_list.append("There Is Not Any Variable Proxy!")
        else:
            if len(proxy_pool_fp.readlines()) < request_num:
                request_num = len(proxy_pool_fp.readlines())
            while len(proxy_list) != request_num:
                proxy_list.append(proxy_pool_fp.readline())
        ThreadLock.VariFileUnLock()
        return proxy_list



#close listener socket -- > self.socket_server and working socket