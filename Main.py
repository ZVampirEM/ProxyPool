#-*- coding=utf-8 -*-

'''
Created on Jul 14, 2016

@author: enming.zhang
'''


from conf import ProxyPoolConfig
from ProxyPoolCollector import ProxyPoolCollectorThread

def main():
    #get headers, url, time_stamp from the module of conf
    config_instance = ProxyPoolConfig.ConfigOperating()
    config_instance.parse_conf_json()
    request_headers = config_instance.get_headers()
    request_url = config_instance.get_url()
    get_proxy_time_stamp = config_instance.get_time_stamp()

    #proxy pool collector thread
    proxy_pool_collector_thread = ProxyPoolCollectorThread.ProxyPoolCollector(request_url,
                                                request_headers, get_proxy_time_stamp)
    proxy_pool_collector_thread.collect_proxy_pool()

    if proxy_pool_collector_thread.is_ready:
        #has variable proxy, start listener thread, whether or not
        pass



    while True:
        terminal_input = raw_input()

        if terminal_input == "exit":
            proxy_pool_collector_thread.join()
            break



if __name__ == '__main__':
    main()