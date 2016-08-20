import socket
import threading
import time
import re
from Lock import ThreadLock
import requests

class Listener(object):
    def __init__(self, listen_addr, listen_port, sf_name, flt_url, filter_headers):
        self.__m_listen_addr = listen_addr
        self.__m_listen_port = listen_port
        self.socket_server = None
        self.__m_send_proxy_list = []
        self.__proxy_save_file = sf_name
        self.__m_filter_url = flt_url
        self.__m_headers = filter_headers
        self.__m_filter_session = requests.session()
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
                print self.__m_send_proxy_list

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
        ThreadLock.Lock()
        proxy_pool_fp = open(self.__proxy_save_file, 'r')
#        print len(proxy_pool_fp.readlines())
        while len(proxy_list) != request_num:
            proxy_ele = proxy_pool_fp.readline()
            print proxy_ele
            filter_result = self.FilterProxy(proxy_ele)
            if filter_result == True:
                proxy_list.append(proxy_ele)
            else:
                continue
        ThreadLock.UnLock()
        return proxy_list



#close listener socket -- > self.socket_server and working socket