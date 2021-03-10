import tkinter as tk
import tkinter.ttk as ttk


class MainFrame(ttk.Frame):
    def __init__(self, master: tk.Misc):
        ttk.Frame.__init__(self, master)

        self.init_ui()

    def init_ui(self):
        for i in range(5):
            ttk.Label(self, text=_("test 123: ")).grid(row=i, column=0)
            ttk.Label(self, text="test value").grid(row=i, column=1)
