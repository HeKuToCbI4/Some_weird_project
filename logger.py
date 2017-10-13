from threading import Lock
from helper import LogClass
from inspect import currentframe, getframeinfo


class Logger:
    def __init__(self, name='Default Logger', log_class=None, log_script_information=True, lock=None,
                 log_to_file=False, log_name=None, always_log_to_file=True):
        self._log_class = log_class
        self._name = name
        self._log_script_information = log_script_information
        self._lock = lock if lock is not None else Lock()
        self._log_to_file = log_to_file
        self._log_file_name = log_name
        self._always_log_to_file = always_log_to_file

    def log_string(self, log_class, string):
        if log_class >= self._log_class:
            frame_info = getframeinfo(currentframe().f_back)
            if self._log_script_information:
                string = '[{file_name}] ({line_number}) {logger_name} {string}:'.format(file_name=frame_info.filename,
                                                                                        line_number=frame_info.lineno,
                                                                                        logger_name=self._name,
                                                                                        string=string)
            else:
                string = '{logger_name} {string}:'.format(logger_name=self._name, string=string)
            print(string)
            