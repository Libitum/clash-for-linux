from clashtk.core.binary_manager import BinaryManager
from clashtk.core.config import Config

_bm = BinaryManager(Config('test_config'))


class TestBinaryManager:
    def test_upzip(self):
        _bm.upgrade('v1.4.2')
        assert 'v1.4.2' == _bm.get_version()
