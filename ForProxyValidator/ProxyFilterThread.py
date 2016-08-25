#-*- coding=utf-8 -*-

'''
Created on Aug 23, 2016

@author: enming.zhang
'''

import ProxyFilter
from ThreadBase import ThreadBaseModule

class FilterThread(ThreadBaseModule.OriginalThread):
    def __init__(self):
        self.m_filter_instance = ProxyFilter.Filter()
        ThreadBaseModule.OriginalThread.__init__(self)
        
    def Initialize(self):
        return True
    
    def Run(self):
        self.m_filter_instance.filter_variable_proxy()
    
    def ExitInstance(self):
        return True