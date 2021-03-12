from concurrent import futures


class ClashService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClashService, cls).__new__(cls)
            cls._instance._init_()
        return cls._instance

    # Self defined initialization method for singleton.
    def _init_(self):
        self.threadpool = futures.ThreadPoolExecutor(5, "clash-")

    def start_to_get_current_version(self):
        pass
