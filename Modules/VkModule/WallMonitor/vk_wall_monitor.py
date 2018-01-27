import queue
from threading import Thread, Event

from Modules.Common.checker import Failure
from Modules.Common.helper import LogClass
from Modules.Common.logger import Logger
from Modules.DataBaseModule.bot_database import BotDatabase
from Modules.VkModule.vk_module import VkModule
import time
from Modules.Common.url_validator import URLValidator

class VkWallMonitor:
    """
    Class used to monitor wall activities on desired domains.
    """
    def __init__(self, vk_api):
        self._vk_api = vk_api
        self._db_provider = BotDatabase()
        query_result = self._db_provider.get_all_domains()
        self._monitored_domains = []
        for domain in query_result:
            self._monitored_domains.append(*domain)
        self.logger = Logger(name='VK Logger')
        self._pause_monitoring = Event()
        self._stop_monitoring = Event()
        self._updates_queue = queue.Queue()
        self._url_validator = URLValidator()

    def add_domain(self, domain):
        vk_url = 'https://vk.com/' + domain
        if self._url_validator.validate_url(vk_url):
            if not domain in self._monitored_domains:
                self._monitored_domains.append(domain)
                self._db_provider.add_domain(domain)
                self.monitor_wall(domain)
        else:
            self.logger.log_string(LogClass.Info, 'Invalid domain {} entered!'.format(domain))

    def get_last_wall_post(self, owner_id=0, domain=None, **kwargs):
        return self.get_n_last_wall_posts(owner_id, domain, 1, **kwargs)[0]

    def get_n_last_wall_posts(self, owner_id=0, domain=None, count=1, **kwargs):
        destination = 'destination {}, with {}'.format(owner_id if domain is None else domain, kwargs.keys())
        self.logger.log_string(LogClass.Info, "Sending 'get wall posts' request to {}".format(destination))
        if domain is None:
            response = self._vk_api.wall.get(owner_id=owner_id, count=count, **kwargs)
        else:
            response = self._vk_api.wall.get(domain=domain, count=count, **kwargs)
        self.logger.log_string(LogClass.Info, "Got response from {}".format(destination, response))
        if response['items']:
            return response['items']
        else:
            message = 'Something gone wrong during request to {}.'.format(destination)
            self.logger.log_string(LogClass.Exception, message)
            raise Failure(message)

    def run_monitor_thread(self, domain):
        t = Thread(target=self.monitor_wall, args=domain, daemon=True)
        t.start()

    def monitor_wall(self, domain):
        # TODO: Продумать структуру класса...
        self.logger.log_string(LogClass.Info, 'Starting monitoring of {}'.format(domain))
        # Setup
        last_posts_id = []
        last_20_posts = self.get_n_last_wall_posts(domain=domain, count=20)
        for post in last_20_posts:
            last_posts_id.append(post['id'])
        while not self._stop_monitoring.isSet:
            while not self._pause_monitoring.isSet and not self._stop_monitoring.isSet:
                time.sleep(60)
                last_posts = self.get_n_last_wall_posts(domain=domain, count=10)
                for post in last_posts:
                    if not post['id'] in last_posts_id:
                        self._updates_queue.put({domain: post})
                        last_posts_id.append(post['id'])

    def pause_monitoring(self):
        self.logger.log_string(LogClass.Info, 'Monitoring of vk wall posts is paused.')
        if not self._pause_monitoring.isSet:
            self._pause_monitoring.set()

    def resume_monitoring(self):
        if self._pause_monitoring.isSet():
            self.logger.log_string(LogClass.Info, 'Monitoring of vk wall posts continued.')
            self._pause_monitoring.clear()

    def stop_monitoring(self):
        self._stop_monitoring.set()


if __name__ == '__main__':
    monitor = VkWallMonitor(VkModule().api)
    monitor.add_domain('nycoffee_samara')
    monitor.add_domain('loloveless')
    monitor.add_domain('ASJGOAISHOIASIJHOIA')
