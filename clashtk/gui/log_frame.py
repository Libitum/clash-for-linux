import tkinter as tk
import tkinter.ttk as ttk

from clashtk.core.clash_service import ClashService


class LogFrame(ttk.Frame):
    def __init__(self, master: tk.Misc):
        ttk.Frame.__init__(self, master)

        self._log_fetcher = ClashService().log_service

        self._init_ui()
        self._init_event()

    def _init_ui(self):
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._listbox = tk.Text(self, yscrollcommand=scrollbar.set)
        self._listbox.pack(fill=tk.BOTH)
        scrollbar.config(command=self._listbox.yview)

    def _init_event(self):
        self.after(1000, self._check_log)

    def add_log(self, content):
        self._listbox.insert(tk.END, content + "\n")

    def _check_log(self):
        log = self._log_fetcher.get()
        self._listbox.config(state=tk.NORMAL)
        while log:
            self.add_log(log['payload'])
            log = self._log_fetcher.get()

        self._listbox.config(state=tk.DISABLED)
        self.after(1000, self._check_log)
