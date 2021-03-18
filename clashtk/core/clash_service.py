from clashtk.core.binary_manager import BinaryManager
from clashtk.core.config import Config


class ClashService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClashService, cls).__new__(cls)
            cls._instance._init_()
        return cls._instance

    # Self defined initialization method for singleton.
    def _init_(self, config: Config = None):
        self.config = config or Config()
        self.binary_manager = BinaryManager(self.config)
