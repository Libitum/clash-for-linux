import platform
import tkinter as tk

from .sidemenu import SideMenu
from .config_frame import ConfigFrame
from .main_frame import MainFrame


_MAIN_FRAMES = {
    'main': MainFrame,
    'config': ConfigFrame
}


class App(tk.Tk):
    def __init__(self, hide: bool = False) -> None:
        tk.Tk.__init__(self)

        self.title = f"Clash For {platform.system()}"

        self._frame = None

        # TODO: iconify the window if started automatically.
        self.init_ui()

    def init_ui(self) -> None:
        side_menu = SideMenu(self)
        side_menu.pack(side=tk.LEFT)

        self.change_frame('main')

    def change_frame(self, frame_name: str):
        if self._frame:
            self._frame.destroy()
        self._frame = _MAIN_FRAMES[frame_name](self)
        self._frame.pack(expand=True)

    def run(self):
        self.mainloop()
