#-*- coding=utf-8 -*-

'''
Created on Aug 23, 2016

@author: enming.zhang
'''

import time
import os
import re
from conf import ProxyPoolConfig
from Lock import ThreadLock

class Filter(object):
    def __init__(self):
        self.__m_filter_headers = ProxyPoolConfig.config_instance.get_filter_headers
        self.__m_filter_url_one = ProxyPoolConfig.config_instance.get_filter_url_1
        self.__m_filter_url_two = ProxyPoolConfig.config_instance.get_filter_url_2
        self.__m_filter_url_thr = ProxyPoolConfig.config_instance.get_filter_url_3

    def find_write_file(self):
        is_today_file_exist_flag = False
        today = str(int(time.strftime("%Y%m%d", time.localtime(time.time()))))
        today_file_name = 'VariableProxy' + today + '.txt'
        file_list_in_current_dir = os.listdir(os.getcwd())
        varifile_pattern = re.compile(r'VariableProxy\d{8}\.txt')
        for file_name in file_list_in_current_dir:
            file_name_match = varifile_pattern.match(file_name)
            if file_name_match:
                if file_name != today_file_name:
                    os.remove(file_name)
                else:
                    is_today_file_exist_flag = True

        if not is_today_file_exist_flag:
            today_varifile_handle = open(today_file_name, 'w')
            today_varifile_handle.close()
        return today_file_name


    def filter_variable_proxy(self):
        variable_proxy_file = self.find_write_file()
        proxy_source_file = ProxyPoolConfig.config_instance.get_savefile_name
        ThreadLock.SaveFileLock()
        try:
            source_file_handle = open(proxy_source_file, 'r')
        except:
            print "{0} haven't been created!".format(proxy_source_file)
        else:
            all_proxy_list = source_file_handle.readlines()
            source_file_handle.close()
            print all_proxy_list
            print len(all_proxy_list)
        ThreadLock.SaveFileUnLock()



        # for proxy_item in all_proxy_list:
        #     print proxy_item

#     def FilterProxy(self, proxy):
#         proxy_under_test = dict(http = proxy[:-1])
#         print proxy_under_test
#         try:
#             rtn_obj = self.__m_filter_session.get(self.__m_filter_url, headers = self.__m_headers, proxies = proxy_under_test, timeout = 5)
#             print rtn_obj.status_code
#             print rtn_obj.ok
#             if rtn_obj.ok:
#                 print "proxy {0} work!".format(proxy[:-1])
#                 return True
#             else:
#                 print "proxy {0} can't work".format(proxy[:-1])
#                 return False
#         except:
# #            print rtn_obj.status
#             print "proxy {0} can't work".format(proxy[:-1])
#             return False