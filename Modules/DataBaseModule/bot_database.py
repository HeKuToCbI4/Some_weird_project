from Modules.Common.checker import Failure
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
                             log_to_file=True, log_name='bot_database_log.txt')

    def get_city_id_by_name(self, city):
        return self._cursor.execute('SELECT id FROM cities WHERE name=?', (city,))

    def get_wall_id_by_domain(self, domain):
        return self._cursor.execute('SELECT id FROM vk_walls WHERE domain=?', (domain,))

    def get_weather_subscriptions(self, chat_id):
        return self._cursor.execute('SELECT * FROM weather_subscriptions WHERE id_chat=?', (chat_id,))

    def get_vk_subscriptions(self, chat_id):
        return self._cursor.execute('SELECT * FROM vk_wall_subscriptions WHERE id_chat=?', (chat_id,))

    def get_domain_by_id(self, domain_id):
        return self._cursor.execute('SELECT domain FROM vk_walls WHERE id=?', (domain_id,))

    def get_city_by_id(self, city_id):
        return self._cursor.execute('SELECT name FROM cities WHERE id=?', (city_id,))

    def add_weather_subscription(self, chat_id, city):
        self.logger.log_string(LogClass.Trace,
                               'Attempting to add chat {} subscription on {} to table weather_subscriptions.'.format(
                                   chat_id, city))
        try:
            query_result = self.get_city_id_by_name(city).fetchone()
            if query_result is None:
                self.add_city(city)
                query_result = self.get_city_id_by_name(city).fetchone()
            self._cursor.execute('INSERT INTO weather_subscriptions(id_chat, id_city) VALUES (?,?)',
                                 (chat_id, query_result))
            self.commit_chages()
        except BaseException as e:
            error_msg = 'Error {} during adding chat {} weather subscription on {} to database.'.format(e, chat_id,
                                                                                                        city)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        self.logger.log_string(LogClass.Trace,
                               'Chat {} successfully subscribed to weather in {}/database.'.format(chat_id, city))

    def add_chat(self, chat_id, last_active):
        self.logger.log_string(LogClass.Trace, 'Attempting to add chat {} to table chats.'.format(chat_id))
        try:
            query_result = self._cursor.execute('SELECT * FROM chats WHERE id_chat=?', chat_id)
            if query_result is None:
                self._cursor.execute('INSERT INTO chats VALUES (?,?)', (chat_id, last_active))
                self.commit_chages()
        except BaseException as e:
            error_msg = 'Error {} during adding chat {} to database.'.format(e, chat_id)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        self.logger.log_string(LogClass.Trace, 'Chat {} successfully added to database.'.format(chat_id))

    def add_city(self, city):
        self.logger.log_string(LogClass.Trace, 'Attempting add {} to table cities'.format(city))
        try:
            if self.get_city_id_by_name(city).fetchone() is None:
                self._cursor.execute('INSERT INTO cities(name) VALUES (?)', (city,))
                self.commit_chages()
        except BaseException as e:
            error_msg = 'Error {} during adding city {} to table cities'.format(e, city)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        self.logger.log_string(LogClass.Trace, 'City {} successfully added to database.'.format(city))

    def add_vk_domain_subscription(self, chat_id, domain):
        self.logger.log_string(LogClass.Trace,
                               'Attempting to add chat {} subscription on {} to table vk_walls_subscription.'.format(
                                   chat_id, domain))
        try:
            query_result = self.get_wall_id_by_domain(domain).fetchone()
            if query_result is None:
                self.add_domain(domain)
                query_result = self.get_city_id_by_name(domain).fetchone()
            self._cursor.execute('INSERT INTO vk_wall_subscriptions(id_chat, id_domain) VALUES (?,?)',
                                 (chat_id, query_result))
            self.commit_chages()
        except BaseException as e:
            error_msg = 'Error {} during adding chat {} subscription on {} to database.'.format(e, chat_id, domain)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        self.logger.log_string(LogClass.Trace,
                               'Chat {} successfully subscribed to wall {}/database.'.format(chat_id, domain))

    def remove_city(self, city):
        self.logger.log_string(LogClass.Trace, 'Attempting deletion of {} city from cities'.format(city))
        try:
            self._cursor.execute('DELETE FROM cities WHERE name=?', (city,))
            self.commit_chages()
        except BaseException as e:
            error_msg = 'Error {} occurred during deleting {} from cities'.format(e, city)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        self.logger.log_string(LogClass.Trace, 'City {} successfully removed from database.'.format(city))

    def add_domain(self, domain):
        self.logger.log_string(LogClass.Trace, 'Attempting add {} to table vk_walls'.format(domain))
        try:
            if self.get_wall_id_by_domain(domain).fetchone() is None:
                self._cursor.execute('INSERT INTO vk_walls(domain) VALUES (?)', (domain,))
                self.commit_chages()
        except BaseException as e:
            error_msg = 'Error {} during adding domain {} to table vk_walls'.format(e, domain)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        self.logger.log_string(LogClass.Trace, 'Domain {} successfully added to database.'.format(domain))

    def remove_domain(self, domain):
        self.logger.log_string(LogClass.Trace, 'Attempting deletion of {} domain from vk_walls'.format(domain))
        try:
            self._cursor.execute('DELETE FROM vk_walls WHERE domain=?', (domain,))
            self.commit_chages()
        except BaseException as e:
            error_msg = 'Error {} occurred during deleting {} from vk_walls'.format(e, domain)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        self.logger.log_string(LogClass.Trace, 'Domain {} successfully removed from database.'.format(domain))

    def remove_vk_domain_subscription(self, chat_id, domain):
        self.logger.log_string(LogClass.Trace,
                               'Attempting deletion of {} subscription to {} from vk_walls_subscriptions'.format(
                                   chat_id, domain))
        try:
            domain_id = self.get_wall_id_by_domain(domain)
            self._cursor.execute('DELETE FROM vk_wall_subscriptions WHERE id_chat=? AND id_domain=?',
                                 (chat_id, domain_id))
            self.commit_chages()
        except BaseException as e:
            error_msg = 'Error {} occurred during deletion of {} subscription to {} from vk_walls_subscriptions'.format(
                e, chat_id, domain)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        self.logger.log_string(LogClass.Trace,
                               'Subscription {} to {} successfully removed from database.'.format(chat_id, domain))

    def remove_weather_subscription(self, chat_id, city):
        self.logger.log_string(LogClass.Trace,
                               'Attempting deletion of {} subscription to weather {} from weather_subscriptions'.format(
                                   chat_id, city))
        try:
            city_id = self.get_city_id_by_name(city)
            self._cursor.execute('DELETE FROM weather_subscriptions WHERE id_chat=? AND id_city=?',
                                 (chat_id, city_id))
            self.commit_chages()
        except BaseException as e:
            error_msg = 'Error {} occurred during deletion of {} subscription to weather in {} from weather_subscriptions'.format(
                e, chat_id, city)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        self.logger.log_string(LogClass.Trace,
                               'Subscription {} to weather in {} successfully removed from database.'.format(chat_id,
                                                                                                             city))

    def get_all_domains(self):
        self.logger.log_string(LogClass.Trace, 'Attempting to get all domains from database')
        try:
            query_result = self._cursor.execute('SELECT domain FROM vk_walls')
        except BaseException as e:
            error_msg = 'Failed to get all domains from vk_walls, {} occurred'.format(e)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        return query_result.fetchall()

    def get_all_cities(self):
        self.logger.log_string(LogClass.Trace, 'Attempting to get all domains from database')
        try:
            query_result = self._cursor.execute('SELECT name FROM cities')
        except BaseException as e:
            error_msg = 'Failed to get all cities, {} occurred'.format(e)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        return query_result.fetchall()


if __name__ == '__main__':
    db = BotDatabase()
    db.stop()
