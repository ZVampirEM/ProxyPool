#-*- coding=utf-8 -*-

'''
Created on Jul 14, 2016

@author: enming.zhang
'''

import time
from ProxyPool import VampirEMProxyPool


def handle_proxy_pool(get_proxy_url, need_headers):
    # create the instance of VampirEMProxyPool
    m_proxy_pool = VampirEMProxyPool(get_proxy_url, need_headers)
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

    handle_proxy_pool(url, headers)



    get_proxy_time_stamp = [235959, 35959, 75959, 115959, 155959, 195959, 81659]

    while 1:
        current_time = int(time.strftime("%H%M%S", time.localtime(time.time())))

        for time_item in get_proxy_time_stamp:
            if (current_time - time_item) in range(-59, 60):
                handle_proxy_pool(url, headers)

#        else:
#            print current_time
#            print "It is not time to get the proxy!!! You can use the proxy in ProxyPool.txt!"


if __name__ == '__main__':
    main()