import abc
import tkinter as tk
import tkinter.ttk as ttk


class NoteBookFrame(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        ttk.Frame.__init__(self, master)

    @abc.abstractmethod
    def enter(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def leave(self):
        raise NotImplementedError()
