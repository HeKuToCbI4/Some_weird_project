import sqlite3

from Modules.Common.helper import LogClass
from Modules.Common.logger import Logger


class DataBase:
    def __init__(self, database, logger=None):
        self.logger = Logger(name='DatabaseLogger', log_class=LogClass.Info, log_script_information=True,
                             log_to_file=True,
                             log_name='database_log.txt') if logger is None else logger
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

    def backup_database(self):
        pass

    def restore_last_working_state(self):
        pass

    def commit_chages(self):
        self.logger.log_string(LogClass.Trace, 'Chages to database saved')
        self._connection.commit()
