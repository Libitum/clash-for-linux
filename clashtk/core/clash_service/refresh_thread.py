import abc
import threading
from typing import List

from clashtk.common.log import logger
from requests.models import HTTPError


class RefreshTaskInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def refresh(self) -> None:
        raise NotImplementedError()


class RefreshThread(object):
    def __init__(self) -> None:
        self._task_list: List = []
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run,
                                        name="RefreshThread", daemon=True)

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()

    def add_task(self, task):
        self._task_list.append(task)

    def _run(self):
        while not self._stop_event.is_set():
            for task in self._task_list:
                try:
                    task.refresh()
                except HTTPError as error:
                    logger.warning(f"Refresh {task} failed: "
                                   f"{error.response.content}")

            self._stop_event.wait(5)
