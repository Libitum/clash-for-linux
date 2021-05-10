import platform
import tkinter as tk
import tkinter.ttk as ttk

from clashtk.core.clash_service import ClashService

from .log_frame import LogFrame
from .proxy_frame import ProxyFrame
from .status_frame import StatusFrame
from .tools import async_executor
from .top_frame import TopFrame


class App(tk.Tk):
    def __init__(self, hide: bool = False) -> None:
        tk.Tk.__init__(self)
        self.title(f"Clash For {platform.system()}")

        self._frame = None

        clash_service = ClashService()
        clash_service.start()

        async_executor.AsyncExecutor().init(self)
        # TODO: iconify the window if started automatically.
        self.init_ui()

    def init_ui(self) -> None:
        TopFrame(self).pack(side=tk.TOP, fill=tk.X, expand=tk.YES)

        nb = ttk.Notebook(self, width=1000)
        nb.add(StatusFrame(nb), text="Status")
        nb.add(ProxyFrame(nb), text="Proxy")
        nb.add(LogFrame(nb), text="Log")

        nb.pack(expand=True, fill=tk.BOTH)

    def run(self):
        self.mainloop()
