import os
import platform


class Config:
    def __init__(self, root: str = None) -> None:
        self._root = root or os.path.join(os.path.expanduser('~'), 'clashtk')
        os.makedirs(self.binary_dir, exist_ok=True)

    @property
    def binary_dir(self):
        return os.path.join(self._root, 'bin')

    @property
    def binary_path(self):
        system_info = platform.system().lower()
        binary_name = 'clash.exe' if system_info == 'windows' else 'clash'
        return os.path.join(self.binary_dir, binary_name)
