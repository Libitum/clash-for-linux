import tkinter as tk
import tkinter.ttk as ttk


class SideMenu(ttk.Frame):
    def __init__(self, master: tk.Misc):
        ttk.Frame.__init__(self, master)

        self.init_ui()

    def init_ui(self) -> None:
        ttk.Button(self, text="Main", command=lambda: self.master.change_frame('main')).pack(fill=tk.X)
        ttk.Button(self, text="Config", command= lambda: self.master.change_frame('config')).pack(fill=tk.X)
