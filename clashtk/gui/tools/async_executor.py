"""
The module for asynchronous running tasks in Tk GUI.
"""
import tkinter as tk
from concurrent import futures
from typing import Any, Callable, List, Optional, Tuple, TypeVar

_THREAD_NUM = 5
_EVENT_PERIOD_MS = 200

T = TypeVar('T')


class AsyncExecutor:
    """
    Used for asynchronous tasks in Tk GUI. It runs task in threads so that
    it would not block GUI thread. It takes use of tk.after to check the
    event and do the callback in the GUI thread, so we can use it just like
    traditional "callback" way.

    The class is singleton, so it's shared in the process.

    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AsyncExecutor, cls).__new__(cls)
        return cls._instance

    def init(self, master: tk.Misc) -> None:
        """ Initialize the singleton with Tk.
        Args:
            master: Same in Tk.
        """
        if getattr(self, '_master', None):
            raise RuntimeError('Can be only initialized once')

        self._threadpool = futures.ThreadPoolExecutor(_THREAD_NUM, "clash-")
        self._event_list: List[
            Tuple[
                futures.Future,
                Callable[[Any], None],
                Optional[Callable[[BaseException], None]]
            ]
        ] = []
        self._master: tk.Misc = master

    def submit(self, task: Callable[[], T],
               on_success: Callable[[T], None],
               on_failure: Callable[[BaseException], None] = None) -> None:
        """
        Submit a task into threadpool, and call the "callback" automatically
        when the task is done.

        Args:
            task: The callable function running in thread.
            on_success: Will run this "on_success" automatically when the task is done.
        """
        if not getattr(self, '_master', None):
            raise RuntimeError('Not initialized. Please call init() at first.')

        future = self._threadpool.submit(task)
        self._event_list.append((future, on_success, on_failure))
        # If the len of event list is 1, means that it's not running.
        if len(self._event_list) == 1:
            self._master.after(_EVENT_PERIOD_MS, self._handle_event)

    def _handle_event(self):
        """ Works as event loop to do the callback. """
        for event in self._event_list:
            future, on_success, on_failure = event
            # TODO: handle exception
            if future.done():
                if future.exception():
                    if on_failure:
                        on_failure(future.exception() or BaseException())
                else:
                    on_success(future.result())
                self._event_list.remove(event)

        # Try to handle events in next cycle.
        if len(self._event_list) > 0:
            self._master.after(_EVENT_PERIOD_MS, self._handle_event)
