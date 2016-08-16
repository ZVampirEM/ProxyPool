#-*- coding=utf-8 -*-

'''
Created on Jul 14, 2016

@author: enming.zhang
'''


from conf import ProxyPoolConfig
from ProxyPoolCollector import ProxyPoolCollectorThread
from RequestProxyListener import RequestProxyListenerThread
import threading

thread_lock = threading.Lock()

def main():
    #get headers, url, time_stamp from the module of conf
    config_instance = ProxyPoolConfig.ConfigOperating()
    config_instance.parse_conf_json()
    request_headers = config_instance.get_headers
    request_url = config_instance.get_url
    get_proxy_time_stamp = config_instance.get_time_stamp
    listen_addr = config_instance.get_listen_addr
    listen_port = config_instance.get_listen_port
    save_file = config_instance.get_savefile_name

    #proxy pool collector thread
    proxy_pool_collector_thread = ProxyPoolCollectorThread.ProxyCollectorThread(request_url,
                                                    request_headers, get_proxy_time_stamp, save_file)
    proxy_pool_collector_thread.launch()

    request_listen_thread = RequestProxyListenerThread.RequestListenerThread(listen_addr, listen_port, save_file)
    request_listen_thread.launch()

    while True:
        terminal_input = raw_input()

        if terminal_input == "exit":
            proxy_pool_collector_thread.Stop()
            break



if __name__ == '__main__':
    main()