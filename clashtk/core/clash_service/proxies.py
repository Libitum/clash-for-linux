from concurrent import futures

import requests
from clashtk.common.config import Config

from .refresh_thread import RefreshTaskInterface


class Proxies(RefreshTaskInterface):
    def __init__(self, config: Config = None,
                 executor: futures.Executor = None) -> None:
        self._config = config or Config()
        self._data = {}

    def refresh(self):
        self._fetch_proxy()

    def proxy_list(self, type='Proxy'):
        proxies = self._data.get('proxies', {})
        return proxies.get(type, None)

    def _fetch_proxy(self):
        url = self._config.control_url + '/proxies'
        res = requests.get(url)
        res.raise_for_status()
        self._data.update(res.json())
