#-*- coding=utf-8 -*-

'''
Created on Jul 14, 2016

@author: enming.zhang
'''
import requests
from bs4 import BeautifulSoup

class VampirEMProxyPool(object):
    __m_target_url = ""
    __m_heads      = {}
    
    def __init__(self, url, heads):
        self.__m_target_url = url
        self.__m_heads = heads
        
    #Parse the url xicidaili.com
    def parse_xici_com(self):
        m_session = requests.session()
        req = m_session.get(self.__m_target_url, headers = self.__m_heads)
        # use beautifulsoup to parse html
        bs = BeautifulSoup(req.text, 'lxml')
        print len(bs.select('body #wrapper #body #ip_list .odd'))

        
        