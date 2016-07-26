#-*- coding=utf-8 -*-

'''
Created on Jul 14, 2016

@author: enming.zhang
'''

import time
import ProxyPool# import VampirEMProxyPool


def handle_proxy_pool(get_proxy_url, need_headers):
    # create the instance of VampirEMProxyPool
    m_proxy_pool = ProxyPool.VampirEMProxyPool(get_proxy_url, need_headers)
    # parse the xicidaili.com
    m_proxy_pool.parse_xici_com()
    # Verify the proxy is available or not, and save the available proxy in a txt file
    #   m_proxy_pool.abstract_proxy_available()
    m_proxy_pool.save_proxy()


def main():
    
    headers = {
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
             'Accept-Encoding': 'gzip, deflate, sdch',
             'Accept-Language': 'zh-CN,zh;q=0.8',
             'Connection': 'keep-alive',
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
             }

    url = "http://www.xicidaili.com/nn/"

    is_first_get = True

    #Get Proxy Time Point
    get_proxy_time_stamp = {2359: 235953, 359: 35959, 759: 75959, 1159: 115959, 1559: 155959, 1959: 195959}

    #Get Proxy any time when program start
    handle_proxy_pool(url, headers)

    while 1:
        current_time = int(time.strftime("%H%M%S", time.localtime(time.time())))
        find_key = int(time.strftime("%H%M", time.localtime(time.time())))

        if find_key in get_proxy_time_stamp:
            print "it's time"
            if (current_time - get_proxy_time_stamp[find_key]) in range(-5, 6):
                handle_proxy_pool(url, headers)

        time.sleep(10)



if __name__ == '__main__':
    main()