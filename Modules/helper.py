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
    def __init__(self,
                 configuration_path=os.path.join(os.path.dirname(os.getcwd()), 'Configurations', 'configuration.yaml')):
        try:
            with open(configuration_path, 'r') as config_yaml:
                self._config = yaml.load(config_yaml)

        except yaml.YAMLError as yaml_err:
            raise yaml_err

    @property
    def cfg(self):
        return self._config
