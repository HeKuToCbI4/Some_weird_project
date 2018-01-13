import os
from threading import Lock

import yaml


class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = Lock()

    def next(self):
        with self._lock:
            self._value += 1
            return self._value


class LogClass:
    Trace = 1
    Info = 2
    Warning = 3
    Exception = 4


class Configuration:
    __instance = None

    @property
    def cfg(self, custom_configuration_path=None):
        configuration_path = os.path.join(os.path.dirname(os.getcwd()), 'Configurations',
                                          'configuration.yaml') if custom_configuration_path is None else custom_configuration_path
        if self.__instance is None:
            try:
                with open(configuration_path, 'r') as config_yaml:
                    self._config = yaml.load(config_yaml)
            except yaml.YAMLError as yaml_err:
                raise yaml_err
        return self.__instance._config
