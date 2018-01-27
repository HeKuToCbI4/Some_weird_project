from Modules.Common.logger import Logger
from queue import Queue
from collections import namedtuple

DomainInfo = namedtuple('DomainInfo', 'domain ')


class VKWallMonitorController:
    def __init__(self):
        self.logger = Logger(name='VK logger')
        self._updates_queue = Queue()
        self._domain_monitor_controllers = {}
