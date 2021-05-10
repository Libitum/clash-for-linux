import subprocess
from typing import Optional

from clashtk.common.config import Config


class ClashProcess(object):
    def __init__(self, config: Config = None) -> None:
        self.config = config or Config()
        self._process: Optional[subprocess.Popen] = None

    def start(self) -> None:
        if self._process and self._process.poll() is None:
            return

        cmd = [self.config.binary_path, '-d', self.config.profile_dir]
        self._process = subprocess.Popen(cmd)

    def stop(self) -> None:
        if not self._process:
            return

        self._process.terminate()
        self._process.wait()
        self._process = None
