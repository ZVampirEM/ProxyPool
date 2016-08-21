#-*- coding=utf-8 -*-

'''
Created on Jul 14, 2016

@author: enming.zhang
'''


from ProxyPoolCollector import ProxyPoolCollectorThread
from RequestProxyListener import RequestProxyListenerThread
import threading

thread_lock = threading.Lock()

def main():
    #proxy pool collector thread
    proxy_pool_collector_thread = ProxyPoolCollectorThread.ProxyCollectorThread()
    proxy_pool_collector_thread.launch()

    request_listen_thread = RequestProxyListenerThread.RequestListenerThread()
    request_listen_thread.launch()

    while True:
        terminal_input = raw_input()

        if terminal_input == "exit":
            proxy_pool_collector_thread.Stop()
            break



if __name__ == '__main__':
    main()