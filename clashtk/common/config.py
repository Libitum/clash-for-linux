import os
import platform


class Config:
    def __init__(self, root: str = None) -> None:
        self._root = root or os.path.join(
            os.path.expanduser('~'), '.config', 'clashtk')
        os.makedirs(self.binary_dir, exist_ok=True)
        os.makedirs(self.profile_dir, exist_ok=True)

    @property
    def binary_dir(self):
        return os.path.join(self._root, 'bin')

    @property
    def binary_path(self):
        system_info = platform.system().lower()
        binary_name = 'clash.exe' if system_info == 'windows' else 'clash'
        return os.path.join(self.binary_dir, binary_name)

    @property
    def profile_dir(self):
        return os.path.join(self._root, 'profiles')

    @property
    def control_address(self):
        return '127.0.0.1:9090'

    @property
    def control_url(self):
        return 'http://' + self.control_address
