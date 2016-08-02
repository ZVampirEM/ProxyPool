#-*- coding=utf-8 -*-

'''
Created on Jul 14, 2016

@author: enming.zhang
'''

import time
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





if __name__ == '__main__':
    main()