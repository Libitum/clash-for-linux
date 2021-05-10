from concurrent import futures

from clashtk.common.config import Config

from .clash_config import ClashConfig
from .clash_process import ClashProcess
from .log_thread import LogThread
from .proxies import Proxies
from .refresh_thread import RefreshThread
from .traffic_thread import TrafficThread


class ClashService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClashService, cls).__new__(cls)
            cls._instance._init_()
        return cls._instance

    # Self defined initialization method for singleton.
    def _init_(self, config: Config = None):
        config = config or Config()
        # Init a thread pool which can be shared by async calls.
        self._thread_pool = futures.ThreadPoolExecutor(3, 'pool-')
        # Used to refresh data periodically.
        self._refresh_thread = RefreshThread()

        self._clash_process = ClashProcess(config)
        self._traffic_thread = TrafficThread(config)
        self._clash_log_thread = LogThread(config)

        self.traffic = self._traffic_thread
        self.clash_log = self._clash_log_thread
        self.clash_config = ClashConfig(config, self._thread_pool)
        self.proxies = Proxies(config, self._thread_pool)

        self._refresh_thread.add_task(self.clash_config)
        self._refresh_thread.add_task(self.proxies)

    def start(self):
        # self.clash_process.start()
        # sleep 0.5s
        self._refresh_thread.start()
        self._traffic_thread.start()
        self._clash_log_thread.start()

    def stop(self):
        self._thread_pool.shutdown(cancel_futures=True)
        # Stop in reverse order.
        self._refresh_thread.stop()
        self._clash_log_thread.stop()
        self._traffic_thread.stop()
        self._clash_process.stop()
