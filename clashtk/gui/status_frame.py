import tkinter as tk
import tkinter.ttk as ttk

from clashtk.common.i18n import _
from clashtk.core import config
from clashtk.core.clash_service import ClashService
from clashtk.gui.tools.async_executor import AsyncExecutor


class StatusFrame(ttk.Frame):
    def __init__(self, master: tk.Misc):
        ttk.Frame.__init__(self, master)

        self._init_var()
        self._init_ui()
        self._init_event()

    def _init_var(self):
        self._current_version = tk.StringVar(self)
        self._latest_version = tk.StringVar(self)

    def _init_ui(self):
        ttk.Label(self, text=_('Running Status')).grid(row=0, column=0)
        ttk.Button(self, text='start').grid(row=0, column=1)

        ttk.Label(self, text=_('Current Version')).grid(row=1, column=0)
        ttk.Label(self, textvariable=self._current_version).grid(row=1, column=1)

        ttk.Label(self, text=_('Latest Version')).grid(row=2, column=0)
        ttk.Label(self, textvariable=self._latest_version).grid(row=2, column=1)

    def _init_event(self):
        self._exector = AsyncExecutor()
        self._clash_service = ClashService()
        self._clash_service._init_(config.Config('test_config'))

        self._exector.submit(self._clash_service.binary_manager.get_version,
                             self._on_current_version_arrived)
        self._exector.submit(self._clash_service.binary_manager.get_latest_version,
                             self._on_latest_version_arrived)

    def _on_current_version_arrived(self, version):
        self._current_version.set(version)

    def _on_latest_version_arrived(self, version):
        self._latest_version.set(version)
