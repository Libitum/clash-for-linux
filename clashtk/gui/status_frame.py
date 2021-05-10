import tkinter as tk
import tkinter.ttk as ttk

from clashtk.common.i18n import _
from clashtk.core.clash_service import ClashService
from clashtk.gui.tools.async_executor import AsyncExecutor


class StatusFrame(ttk.Frame):
    def __init__(self, master: tk.Misc):
        ttk.Frame.__init__(self, master)

        self._init_var()
        self._init_ui()
        self._init_event()

    def _init_var(self):
        # The current version of Clash.
        self._current_version = tk.StringVar(self)
        # The latest version of Clash.
        self._latest_version = tk.StringVar(self)
        # This is for configuration.
        self._alow_lan = tk.BooleanVar(self, value=False)

    def _init_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text=_('Current Version:')).grid(
            row=1, column=0, sticky=tk.E)
        ttk.Label(self, textvariable=self._current_version).grid(
            row=1, column=1)

        ttk.Label(self, text=_('Latest Version:')).grid(
            row=2, column=0, sticky=tk.E)
        ttk.Label(self, textvariable=self._latest_version).grid(
            row=2, column=1)

        ttk.Label(self, text=_('Upgrade Clask:')).grid(
            row=3, column=0, sticky=tk.E)
        self._btn_upgrade = ttk.Button(
            self, text='Upgrade', state=tk.DISABLED, command=self._on_upgrade_clicked)
        self._btn_upgrade.grid(row=3, column=1)

        ttk.Label(self, text=_('Alow Lan:')).grid(row=4, column=0, sticky=tk.E)
        ttk.Checkbutton(self, variable=self._alow_lan,
                        onvalue=True, offvalue=False).grid(row=4, column=1)

        ttk.Label(self, text=_('Port:')).grid(row=5, column=0, sticky=tk.E)
        ttk.Label(self, text="7890").grid(row=5, column=1)

    def _init_event(self):
        self._exector = AsyncExecutor()
        self._clash_service = ClashService()

        #self._exector.submit(self._clash_service.binary_manager.get_version,
        #                     self._on_current_version_arrived)
        #self._exector.submit(self._clash_service.binary_manager.get_latest_version,
        #                     self._on_latest_version_arrived)

    def _on_current_version_arrived(self, version):
        self._current_version.set(version)

    def _on_latest_version_arrived(self, version):
        self._latest_version.set(version)
        if version and version != self._current_version.get():
            self._btn_upgrade['state'] = tk.NORMAL

    def _on_upgrade_clicked(self):
        self._exector.submit(self._clash_service.binary_manager.upgrade,
                             self._on_upgrade_finished)

    def _on_upgrade_finished(self, status):
        self._btn_upgrade['state'] = tk.DISABLED
        self._exector.submit(self._clash_service.binary_manager.get_version,
                             self._on_current_version_arrived)
