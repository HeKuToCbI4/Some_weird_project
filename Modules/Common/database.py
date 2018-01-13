import datetime
import sqlite3

from Modules.Common.helper import Configuration
from Modules.Common.helper import LogClass
from Modules.Common.logger import Logger

cfg = Configuration().cfg


class DataBase:
    def __init__(self, database):
        self.logger = Logger(name='DatabaseLogger', log_class=LogClass.Info, log_script_information=True,
                             log_to_file=True,
                             log_name='database_log_{}.txt'.format(
                                 datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')))
        self.logger.log_string(LogClass.Info, 'Attempting to connect to {}'.format(database))
        try:
            self._connection = sqlite3.connect(database)
        except BaseException as e:
            self.logger.log_string(LogClass.Exception,
                                   '{} occurred during connection to a {} database'.format(e, database))
        self._cursor = self._connection.cursor()

    def stop(self):
        self._connection.close()

    def execute_command(self, command, params=None):
        log_string = 'Executing {} with {} parameters'.format(command, params)
        self.logger.log_string(LogClass.Info, log_string)
        if params is None:
            self._cursor.execute(command)
        else:
            self._cursor.execute(command, params)
