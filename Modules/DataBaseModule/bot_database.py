import datetime

from Modules.Common.database import DataBase
from Modules.Common.helper import Configuration
from Modules.Common.helper import LogClass
from Modules.Common.logger import Logger

cfg = Configuration().cfg


class BotDatabase(DataBase):
    def __init__(self, database=None):
        database_path = database if database is not None else cfg['databases']['default_db']
        super().__init__(database_path)
        self.logger = Logger(name='Bot database logger', log_class=LogClass.Info, log_script_information=True,
                             log_to_file=True, log_name='bot_database_log_{}.txt'.format(
                datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')))

    def add_weather_subscription(self, chat_id, city):
        pass

    def remove_weather_subscription(self, chat_id, city):
        pass

    def add_chat(self, chat_id):
        pass

    def add_city(self, city):
        pass

    def remove_city(self, city):
        pass

    def add_domain(self, domain):
        pass

    def remove_domain(self, domain):
        pass

    def add_vk_domain_subscription(self, chat_id, domain):
        pass

    def remove_vk_domain_subscription(self, chat_id, domain):
        pass

    def backup_database(self):
        pass

    def restore_last_working_state(self):
        pass
