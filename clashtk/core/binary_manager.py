from clashtk.common.exception import ClashTkException
import os
import platform
import subprocess
import zipfile
import gzip
from typing import List, Optional
import stat

import requests

from .config import Config


class BinaryManager:
    def __init__(self, config: Config) -> None:
        self._config = config

    def is_binary_exist(self) -> bool:
        return os.path.exists(self._config.binary_path)

    def get_version(self) -> str:
        """Gets the current binary's version.
        Returns:
            version(str): the current binary's version.
        """
        url = self._config.control_url + '/version'
        res = requests.get(url)
        res.raise_for_status()
        return res.json()['version']

    def get_latest_version(self) -> str:
        """Gets the latest version from github.
        Returns:
            version(str): the latest version from github.
        """
        url = "https://api.github.com/repos/Dreamacro/clash/releases/latest"
        res = requests.get(url)
        res.raise_for_status()
        return res.json()['tag_name']

    def upgrade(self, version: Optional[str] = None) -> None:
        """Upgrades to the latest or specified version.
        Args:
            version(Optional[str]): the specified version that upgrade to.
        """
        version = version or self.get_latest_version()
        if not version:
            # There is no legal latest version exist, so just return.
            return

        current_version = self.get_version()
        # If the current version is same with the target version, just return.
        if version == current_version:
            return

        url = self._generate_download_url(version)
        zip_file = self._download(url)
        binary_path = self._unzip_file(zip_file)

        os.replace(binary_path, self._config.binary_path)
        os.chmod(self._config.binary_path, stat.S_IEXEC)

    def _generate_download_url(self, version: str) -> str:
        system_info = platform.system().lower()
        arch_info = platform.machine().lower()
        format = 'zip' if system_info == 'windows' else 'gz'

        if arch_info == 'x86_64':
            arch_info = 'amd64'

        # TODO: Only support windows right now.
        url = ("https://github.com/Dreamacro/clash/releases/download/"
               f"{version}/clash-{system_info}-{arch_info}-{version}.{format}")

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
        else:
            try:
                extracted_file = os.path.splitext(file_path)[0]
                with gzip.open(file_path, 'rb') as gz, open(extracted_file, 'wb') as fh:
                    while True:
                        data = gz.read(10240)
                        if data:
                            fh.write(data)
                        else:
                            break

            except gzip.BadGzipFile:
                extracted_file = None

        if extracted_file:
            os.remove(file_path)
            return extracted_file
        else:
            raise ClashTkException(f'Unzip file failed: {file_path}.')
