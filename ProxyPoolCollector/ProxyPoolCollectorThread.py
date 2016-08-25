from ThreadBase import ThreadBaseModule
import ProxyCollector

class ProxyCollectorThread(ThreadBaseModule.OriginalThread):
    def __init__(self):
        self.proxy_pool_collect_instance = ProxyCollector.Collector()
        ThreadBaseModule.OriginalThread.__init__(self)

    def Initialize(self):
        return True

    def Run(self):
        self.proxy_pool_collect_instance.get_proxy_pool()

    def ExitInstance(self):
        del self.proxy_pool_collect_instance

    def Stop(self):
        self.proxy_pool_collect_instance.set_is_to_exit_flag(True)
        self.thread_instance.join()

    def IsOk(self):
        return self.proxy_pool_collect_instance.get_can_handle_flag()