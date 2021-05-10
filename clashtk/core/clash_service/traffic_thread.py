import json
import threading

import requests
from clashtk.common.config import Config


class TrafficThread(object):
    def __init__(self, config: Config = None) -> None:
        self._config = config or Config()

        self._thread = threading.Thread(target=self._fetch_traffic_info,
                                        name="TrafficFetcher",
                                        daemon=True)
        self._lock = threading.Lock()
        self._stop_event = threading.Event()

        self._traffic_info = {
            'up': 0,
            'down': 0
        }

    def start(self):
        self._stop_event.clear()
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

    def get_traffic_info(self):
        with self._lock:
            return self._traffic_info

    def update_traffic_info(self, traffic_info):
        with self._lock:
            self._traffic_info = traffic_info

    def _fetch_traffic_info(self):
        url = self._config.control_url + '/traffic'
        with requests.get(url, stream=True) as stream:
            for chunk in stream.iter_content(chunk_size=None):
                if self._stop_event.is_set():
                    break
                traffic_info = json.loads(chunk)
                self.update_traffic_info(traffic_info)
