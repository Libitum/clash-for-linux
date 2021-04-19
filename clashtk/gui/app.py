import platform
import tkinter as tk
import tkinter.ttk as ttk

from .log_frame import LogFrame
from .status_frame import StatusFrame
from .tools import async_executor
from .traffic_frame import TrafficFrame


class App(tk.Tk):
    def __init__(self, hide: bool = False) -> None:
        tk.Tk.__init__(self)
        self.title(f"Clash For {platform.system()}")

        self._frame = None

        async_executor.AsyncExecutor().init(self)
        # TODO: iconify the window if started automatically.
        self.init_ui()

    def init_ui(self) -> None:
        TrafficFrame(self).pack(side=tk.TOP, fill=tk.X)

        nb = ttk.Notebook(self, width=500)
        nb.add(StatusFrame(nb), text="Status")
        nb.add(LogFrame(nb), text="Log")

        nb.pack(expand=True, fill=tk.BOTH)

    def run(self):
        self.mainloop()
