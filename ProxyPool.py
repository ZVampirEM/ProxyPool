#-*- coding=utf-8 -*-

'''
Created on Jul 14, 2016

@author: enming.zhang
'''
import requests
import re
import time
from bs4 import BeautifulSoup

class VampirEMProxyPool(object):
    __m_target_url = ""
    __m_heads      = {}
    __m_proxy_pool = []
    
    def __init__(self, url, heads):
        self.__m_target_url = url
        self.__m_heads = heads
        
    #Parse the url xicidaili.com
    def parse_xici_com(self):
        # the regular expression which is used to abstract the ip of proxy
        proxy_ip_re_pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
        # the regular expression which is used to abstract the verification time of proxy
        proxy_verf_time_pattern2 = re.compile(r'\d+\-\d+\-\d+')
        # get the local time
        local_time = int(time.strftime('%Y%m%d', time.localtime(time.time())))
        is_last_two_days_flag = True
        page_number = 1
        visit_page_url = self.__m_target_url + str(page_number)
        
        m_session = requests.session()
        while is_last_two_days_flag:
            req = m_session.get(visit_page_url, headers = self.__m_heads)
            # use beautifulsoup to parse html
            bs = BeautifulSoup(req.text, 'lxml')

            for item in bs.select('body #wrapper #body #ip_list tr')[1:]:
                # get the verification time of proxy from html
                orig_verf_time = item.find(text = proxy_verf_time_pattern2)
                # handle the verification time for campare with local time
                handled_veri_time = int('20' + ''.join(orig_verf_time.split(' ')[0].split('-')))
                # just abstract the proxy ip which is verified in the last two days
                if (handled_veri_time == local_time) or (handled_veri_time == local_time - 1): 
                    # abstract the ip and port of proxy from html
                    proxy_ip = item.find(text = proxy_ip_re_pattern)
                    proxy_port = item.find_all('td')[2].string
                    proxy = proxy_ip + ":" + proxy_port
            
                    self.__m_proxy_pool.append(proxy)
                
                else:
                    is_last_two_days_flag = False
                    break
                
            if is_last_two_days_flag:
                page_number += 1
                visit_page_url = self.__m_target_url + str(page_number)
                print 'get page %d' % (page_number)
        
        print len(self.__m_proxy_pool)
        return
        