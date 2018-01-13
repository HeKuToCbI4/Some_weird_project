import os
from threading import Lock
from Modules.Common.checker import Failure

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
        configuration_path = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'Configurations',
                                          'configuration.yaml') if custom_configuration_path is None else custom_configuration_path
        if Configuration.__instance is None:
            Configuration.__instance = Configuration()
            try:
                with open(configuration_path, 'r') as config_yaml:
                    Configuration.__instance._config = yaml.load(config_yaml)
            except yaml.YAMLError as yaml_err:
                raise Failure('{} occurred during config initialization.'.format(yaml_err))
        return Configuration.__instance._config
