import json
import queue
import threading
import time

import requests
from clashtk.core.config import Config


class LogFetcherThread(object):
    def __init__(self, config: Config = None) -> None:
        self._config = config or Config()

        self._thread = threading.Thread(target=self._fetch_log_info,
                                        name="Thread-TrafficFetcher",
                                        daemon=True)

        self._queue = queue.Queue(50)

        self._thread.start()

    def get(self):
        try:
            return self._queue.get_nowait()
        except queue.Empty:
            return None

    def _fetch_log_info(self):
        time.sleep(1)   # To make sure that the clash process is ready.
        url = self._config.control_url + '/logs'
        with requests.get(url, stream=True) as stream:
            for chunk in stream.iter_content(chunk_size=None):
                log = json.loads(chunk)
                self._queue.put_nowait(log)
