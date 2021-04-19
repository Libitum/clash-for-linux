import subprocess
from typing import Optional

from clashtk.core.binary_manager import BinaryManager
from clashtk.core.config import Config
from clashtk.core.log_fetcher import LogFetcherThread
from clashtk.core.traffic_fetcher import TrafficFetcherThread


class ClashService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClashService, cls).__new__(cls)
            cls._instance._init_()
        return cls._instance

    # Self defined initialization method for singleton.
    def _init_(self, config: Config = None):
        self._clash_process: Optional[subprocess.Popen] = None
        self.config = config or Config()
        self.binary_manager = BinaryManager(self.config)
        self.traffic_service = TrafficFetcherThread(self.config)
        self.log_service = LogFetcherThread(self.config)

    def start(self):
        if self._clash_process:
            return

        cmd = [self.config.binary_path, '-d', self.config.profile_dir]
        self._clash_process = subprocess.Popen(cmd)

    def stop(self):
        if not self._clash_process:
            return

        self._clash_process.terminate()
        self._clash_process.wait()
        self._clash_process = None

    def is_running(self) -> bool:
        if not self._clash_process:
            return False

        return self._clash_process.poll() is None
