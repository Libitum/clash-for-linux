import threading
from concurrent import futures

import requests
from clashtk.common.config import Config

from .refresh_thread import RefreshTaskInterface


class ClashConfig(RefreshTaskInterface):
    def __init__(self, config: Config = None,
                 executor: futures.Executor = None) -> None:
        self._config = config or Config()
        self._executor = executor or futures.ThreadPoolExecutor(1)
        self._data = {}
        self._lock = threading.Lock()

    def refresh(self) -> None:
        self._fetch_config()

    @property
    def mode(self) -> str:
        with self._lock:
            return self._data.get('mode', 'Driect')

    @property
    def allow_lan(self) -> bool:
        with self._lock:
            return self._data.get('allow-lan', False)

    def set_config_async(self) -> futures.Future:
        # TODO: implement feature.
        return futures.Future()

    def _fetch_config(self):
        url = self._config.control_url + '/configs'
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        with self._lock:
            self._data.update(data)
