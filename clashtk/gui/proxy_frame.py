import tkinter as tk
import tkinter.ttk as ttk

from clashtk.core.clash_service import ClashService
from clashtk.gui.tools.async_executor import AsyncExecutor


class ProxyFrame(ttk.Frame):
    def __init__(self, master: tk.Misc):
        ttk.Frame.__init__(self, master)

        self._init_event()

    def _init_event(self):
        self._exector = AsyncExecutor()
        self._clash_service = ClashService()

        self._update_proxy_info()

    def _update_proxy_info(self):
        proxy_info = self._clash_service.proxies.proxy_list()
        if proxy_info:
            for proxy in proxy_info['all']:
                ttk.Label(self, text=proxy).pack()
        else:
            self.after(200, self._update_proxy_info)
