#-*- coding=utf-8 -*-

'''
Created on Aug 23, 2016

@author: enming.zhang
'''

import time
import os
import re
import requests
from conf import ProxyPoolConfig
from Lock import ThreadLock

class Filter(object):
    def __init__(self):
        self.__m_filter_headers = ProxyPoolConfig.config_instance.get_filter_headers
        self.__m_filter_url_1 = ProxyPoolConfig.config_instance.get_filter_url_1
        self.__m_filter_url_2 = ProxyPoolConfig.config_instance.get_filter_url_2
        self.__m_filter_url_3 = ProxyPoolConfig.config_instance.get_filter_url_3
        self.__m_filter_session = requests.session()
        self.__m_filter_url_dict = {0: self.__m_filter_url_1, 1: self.__m_filter_url_2, 2: self.__m_filter_url_3}

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

    def IsVariable(self, proxy, serial_no):
        proxy_under_test = dict(http = proxy[:-2])
        filter_url = self.__m_filter_url_dict[serial_no % 3]
        print proxy_under_test
        print filter_url
        
        try:
            rtn_obj = self.__m_filter_session.get(filter_url, headers = self.__m_filter_headers, proxies = proxy_under_test, timeout = 5)
#            print rtn_obj.status_code
#            print rtn_obj.ok
            if rtn_obj.ok:
#                print "proxy {0} work!".format(proxy[:-1])
                return True
            else:
#                print "proxy {0} can't work".format(proxy[:-1])
                return False
        except:
#            print "proxy {0} can't work".format(proxy[:-1])
            return False



    def filter_variable_proxy(self):
        variable_proxy_file = self.find_write_file()
        proxy_source_file = ProxyPoolConfig.config_instance.get_savefile_name
        all_variable_proxy_list = []
        proxy_serial_num = 0
        with ThreadLock.VariFile_ThreadLock:
            try:
                with open(variable_proxy_file, 'r') as var_proxy_fp:
                    all_variable_proxy_list = var_proxy_fp.readlines()
            except:
                print "Open {0} Fail!".format(variable_proxy_file)
        
        with ThreadLock.SaveFile_ThreadLock:
            try:
                with open(proxy_source_file, 'r') as source_file_handle:
                    all_proxy_list = source_file_handle.readlines()
#                    source_file_handle.close()
#                    print all_proxy_list
#                    print len(all_proxy_list)
            except:
                print "{0} haven't been created!".format(proxy_source_file)
        
        #=======================================================================
        # for item in all_variable_proxy_list:
        #     print "variable proxy " + item
        #=======================================================================
        # varify the proxy in proxy list variable or not
        for proxy_item in all_proxy_list:
            proxy_serial_num += 1
            if self.IsVariable(proxy_item, proxy_serial_num):
                if proxy_item in all_variable_proxy_list:
                    continue
                else:
                    with ThreadLock.VariFile_ThreadLock:
                        try:
                            with open(variable_proxy_file, 'a') as var_proxy_fp:
                                var_proxy_fp.write(proxy_item[:-1])
                        except:
                            print "Close Variable Proxy File Fail!"
            else:
                print "Proxy {0} is Avariable!".format(proxy_item[:-2])
                continue