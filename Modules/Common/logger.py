import os
from inspect import currentframe, getframeinfo
from threading import Lock

from Modules.Common.helper import Configuration

cfg = Configuration().cfg
default_log_location = 'C:/telegram_bot_logs/'


###TODO: add timestamps to logs

class Logger:
    default_log_parameters = cfg['loggers']['default_logger']

    def __init__(self, name='Default Logger', *, log_class=None, log_script_information=None, lock=None,
                 log_to_file=None,
                 log_name=None):
        try:
            os.stat(default_log_location)
        except:
            os.mkdir(default_log_location)
        self._logger_parameters = None
        for logger_params in cfg['loggers'].values():
            if logger_params['name'] == name:
                self._logger_parameters = logger_params
        if self._logger_parameters is None:
            self._logger_parameters = Logger.default_log_parameters
        self._log_class = log_class if log_class is not None else self._logger_parameters['log_class']
        self._name = name
        self._log_script_information = log_script_information if log_script_information is not None else \
            self._logger_parameters['log_script_information']
        self._lock = lock if lock is not None else Lock()
        self._log_to_file = log_to_file if log_to_file is not None else self._logger_parameters['log_to_file']
        self._log_file_name = log_name if log_name is not None else self._logger_parameters['log_name']

    def log_string(self, log_class, message):
        log_message = message.encode().decode('utf-8', 'ignore')
        if log_class >= self._log_class or self._log_to_file:
            frame_info = getframeinfo(currentframe().f_back)
            file_name = frame_info.filename.split('\\')[-1]
            if self._log_script_information:
                string = '[{file_name}] ({line_number}) {logger_name}: {string}'.format(file_name=file_name,
                                                                                        line_number=frame_info.lineno,
                                                                                        logger_name=self._name,
                                                                                        string=log_message)
            else:
                string = '{logger_name}: {string}'.format(logger_name=self._name, string=log_message)
            if log_class >= self._log_class:
                print(string)
            if self._log_to_file:
                with self._lock:
                    with open(os.path.join(default_log_location, self._log_file_name), 'a', encoding='utf-8') as f:
                        f.write(string + '\n')
