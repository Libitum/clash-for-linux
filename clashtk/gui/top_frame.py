import tkinter as tk
import tkinter.ttk as ttk

from clashtk.core.clash_service import ClashService


class TopFrame(ttk.Frame):
    def __init__(self, master: tk.Misc):
        ttk.Frame.__init__(self, master)

        self._init_ui()

    def _init_ui(self):
        TrafficFrame(self).pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        ModeFrame(self).pack(side=tk.LEFT,
                             fill=tk.BOTH, expand=tk.YES, padx=20)


class TrafficFrame(ttk.Frame):
    def __init__(self, master: tk.Misc):
        ttk.Frame.__init__(self, master)

        self._init_var()
        self._init_ui()
        self._init_event()

    def _init_var(self):
        self._traffic_up = tk.StringVar()
        self._traffic_down = tk.StringVar()

    def _init_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text='Up:').grid(row=0, column=0, sticky=tk.E)
        ttk.Label(self, textvariable=self._traffic_up).grid(
            row=0, column=1, sticky=tk.W)

        ttk.Label(self, text='Down:').grid(row=1, column=0, sticky=tk.E)
        ttk.Label(self, textvariable=self._traffic_down).grid(
            row=1, column=1, sticky=tk.W)

    def _init_event(self):
        self._on_traffic_update()

    def _on_traffic_update(self):
        clash_service = ClashService()
        traffic_info = clash_service.traffic.get_traffic_info()
        self._traffic_up.set(f"{traffic_info['up'] / 1024:>5.1f} KB")
        self._traffic_down.set(f"{traffic_info['down'] / 1024:>5.1f} KB")
        self.after(1000, self._on_traffic_update)


class ModeFrame(ttk.Frame):
    def __init__(self, master: tk.Misc):
        ttk.Frame.__init__(self, master)

        self._init_var()
        self._init_ui()

    def _init_var(self):
        self._var_mode = tk.StringVar(self, 'Rule')

    def _init_ui(self):
        for value in ['Rule', 'Global', 'Driect']:
            ttk.Radiobutton(self, text=value, value=value,
                            variable=self._var_mode).pack(side=tk.LEFT, padx=5)
