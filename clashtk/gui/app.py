import platform
import tkinter as tk

from .sidemenu import SideMenu
from .config_frame import ConfigFrame
from .main_frame import MainFrame


_MAIN_FRAMES = {
    'main': MainFrame,
    'config': ConfigFrame
}


class App:
    def __init__(self, hide: bool = False) -> None:
        self._root = tk.Tk()
        self._root.title = f"Clash For {platform.system()}"

        self._frame = None

        # TODO: iconify the window if started automatically.
        self.init_ui()

    def init_ui(self) -> None:
        side_menu = SideMenu(self._root, self)
        side_menu.pack(side=tk.LEFT)

        self.change_frame('main')

    def change_frame(self, frame_name: str):
        if self._frame:
            self._frame.destroy()
        self._frame = _MAIN_FRAMES[frame_name](self._root)
        self._frame.pack(expand=True)

    def run(self):
        self._root.mainloop()
