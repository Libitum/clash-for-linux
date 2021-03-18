import os
import os.path as path


class Config:
    def __init__(self, root: str = None) -> None:
        self._root = root or path.join(path.expanduser('~'), 'clashtk')
        os.makedirs(self.binary_dir, exist_ok=True)

    @property
    def binary_dir(self):
        return path.join(self._root, 'bin')

    @property
    def binary_path(self):
        return path.join(self._root, 'bin', 'clash.exe')
