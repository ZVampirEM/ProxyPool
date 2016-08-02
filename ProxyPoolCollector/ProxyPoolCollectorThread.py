import threading
import ProxyPoolCollecting

class ProxyPoolCollector(object):
    def __init__(self, url, headers, time_stamp):
        self.proxy_pool_collect_instance = ProxyPoolCollecting.ProxyPoolCollect(url, headers, time_stamp)
        self.collect_thread = threading.Thread(target=self.proxy_pool_collect_instance.get_proxy_pool)

    def collect_proxy_pool(self):
        self.collect_thread.start()

