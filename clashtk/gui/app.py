import platform
import tkinter as tk
import tkinter.ttk as ttk

from .config_frame import ConfigFrame
from .status_frame import StatusFrame
from .tools import async_executor


class App(tk.Tk):
    def __init__(self, hide: bool = False) -> None:
        tk.Tk.__init__(self)
        self.title(f"Clash For {platform.system()}")

        self._frame = None

        async_executor.AsyncExecutor().init(self)
        # TODO: iconify the window if started automatically.
        self.init_ui()

    def init_ui(self) -> None:
        nb = ttk.Notebook(self, width=500)
        nb.add(StatusFrame(nb), text="Status")
        nb.add(ConfigFrame(nb), text="Config")

        nb.pack(expand=True, fill=tk.BOTH)

    def run(self):
        self.mainloop()
