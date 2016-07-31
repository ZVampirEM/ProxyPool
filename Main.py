#-*- coding=utf-8 -*-

'''
Created on Jul 14, 2016

@author: enming.zhang
'''

import time
from conf import ProxyPoolConfig
from ProxyPoolCollector import ProxyPool


def handle_proxy_pool(get_proxy_url, need_headers):
    # create the instance of VampirEMProxyPool
    m_proxy_pool = ProxyPool.ProxyPool(get_proxy_url, need_headers)
    # parse the xicidaili.com
    m_proxy_pool.parse_xici_com()
    # Verify the proxy is available or not, and save the available proxy in a txt file
    #   m_proxy_pool.abstract_proxy_available()
    m_proxy_pool.save_proxy()


def main():
    #get headers, url, time_stamp from the module of conf
    config_instance = ProxyPoolConfig.ConfigOperating()
    config_instance.parse_conf_json()
    request_headers = config_instance.get_headers()
    request_url = config_instance.get_url()
    get_proxy_time_stamp = config_instance.get_time_stamp()

    print request_headers
    print request_url
    print get_proxy_time_stamp


    #Get Proxy any time when program start
    handle_proxy_pool(request_url, request_headers)

    while 1:
        current_time = int(time.strftime("%H%M%S", time.localtime(time.time())))
        find_key = time.strftime("%H%M", time.localtime(time.time()))

        if find_key in get_proxy_time_stamp:
            print int(get_proxy_time_stamp[find_key])
            print type(int(get_proxy_time_stamp[find_key]))
            if (current_time - int(get_proxy_time_stamp[find_key])) in range(-5, 6):
                handle_proxy_pool(request_url, request_headers)

        time.sleep(10)



if __name__ == '__main__':
    main()