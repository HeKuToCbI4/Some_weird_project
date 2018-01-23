import queue
from threading import Thread, Event

import requests

from Modules.Common.checker import Failure
from Modules.Common.helper import LogClass
from Modules.Common.logger import Logger
from Modules.DataBaseModule.bot_database import BotDatabase
from Modules.VkModule.vk_module import VkModule


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
        self._updates_queue = queue.Queue()

    def add_domain(self, domain):
        vk_url = 'https://vk.com/' + domain
        self.logger.log_string(LogClass.Info, 'Validation URL {}'.format(vk_url))
        try:
            resp = requests.get(vk_url)
            log_string = 'Status code: {}\tText: {}\tHeaders: {}\t'.format(resp.status_code, resp.text, resp.headers)
            self.logger.log_string(LogClass.Trace, 'Got response from {}: {}'.format(vk_url, log_string))
            if resp.status_code / 100 < 4:
                self.logger.log_string(LogClass.Info, 'Domain {} valid.'.format(domain))
                if not domain in self._monitored_domains:
                    self._monitored_domains.append(domain)
                    self._db_provider.add_domain(domain)
                    self.monitor_wall(domain)
                    # TODO: add logic to monitor it.
            else:
                self.logger.log_string(LogClass.Info, 'Domain {} is invalid!'.format(domain))
        except BaseException as e:
            error_message = '{} occurred during validating {}'.format(e, vk_url)
            self.logger.log_string(LogClass.Exception, error_message)
            raise Failure(error_message)

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
        while not self._pause_monitoring.isSet:
            pass

    def pause_monitoring(self):
        self.logger.log_string(LogClass.Info, 'Monitoring of vk wall posts is paused.')
        if not self._pause_monitoring.isSet:
            self._pause_monitoring.set()

    def resume_monitoring(self):
        if self._pause_monitoring.isSet():
            self.logger.log_string(LogClass.Info, 'Monitoring of vk wall posts continued.')
            self._pause_monitoring.clear()


if __name__ == '__main__':
    monitor = VkWallMonitor(VkModule().api)
    print(monitor.get_last_wall_post(domain='nycoffee_samara'))
