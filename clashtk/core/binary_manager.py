from clashtk.common.exception import ClashTkException
import os
import platform
import subprocess
import zipfile
from typing import List, Optional

import requests

from .config import Config


class BinaryManager:
    def __init__(self, config: Config = None) -> None:
        self._config = config or Config()

    def get_version(self) -> str:
        cmd = self._config.binary_path + ' -v'
        result = subprocess.run(cmd, capture_output=True)
        return result.stdout.split()[1].decode()

    def get_newest_version(self) -> str:
        url = "https://api.github.com/repos/Dreamacro/clash/releases/latest"
        res = requests.get(url)
        res.raise_for_status()
        return res.json()['tag_name']

    def upgrade(self, version: Optional[str] = None) -> None:
        version = version or self.get_newest_version()
        url = self._generate_download_url(version)
        zip_file = self._download(url)
        binary_path = self._unzip_file(zip_file)

        os.replace(binary_path, self._config.binary_path)

    def _generate_download_url(self, version: str) -> str:
        system_info = platform.system().lower()
        arch_info = platform.machine().lower()

        # TODO: Only support windows right now.
        url = ("https://github.com/Dreamacro/clash/releases/download/"
               f"{version}/clash-{system_info}-{arch_info}-{version}.zip")

        return url

    def _download(self, url: str) -> str:
        tmp_file = os.path.join(self._config.binary_dir, 'tmp_binary.zip')
        if os.path.exists(tmp_file):
            os.remove(tmp_file)

        with requests.get(url, stream=True) as stream:
            # total_size = stream.headers.get('content-length')
            with open(tmp_file, 'wb') as fh:
                for chuck in stream.iter_content(chunk_size=10240):
                    fh.write(chuck)

        return tmp_file

    def _unzip_file(self, file_path: str) -> str:
        extracted_file = None
        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path, 'r') as zip:
                extract_path = os.path.dirname(file_path)
                name_list: List[str] = zip.namelist()
                for name in name_list:
                    if name.find('clash') != -1:
                        zip.extract(name, extract_path)
                        extracted_file = os.path.join(extract_path, name)
                        break

        if extracted_file:
            os.remove(file_path)
            return extracted_file
        else:
            raise ClashTkException(f'Unzip file failed: {file_path}.')
