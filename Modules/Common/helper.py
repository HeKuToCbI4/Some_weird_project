import os
from threading import Lock

import yaml

from Modules.Common.checker import Failure
from definitions import ROOT_PATH
from collections import namedtuple

Config = namedtuple('Config', 'public private')

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
    def cfg(self, public_configuration_path=None, private_configuration_path=None):
        configuration_path = os.path.join(ROOT_PATH, 'Configurations',
                                          'configuration.yaml') if public_configuration_path is None else public_configuration_path
        private_config_path = os.path.join(ROOT_PATH, 'Configurations',
                                           'private_configuration.yaml') if private_configuration_path is None else private_configuration_path
        if Configuration.__instance is None:
            Configuration.__instance = Configuration()
            try:
                with open(configuration_path, 'r') as config_yaml:
                    public_config = yaml.load(config_yaml)
                with open(private_config_path, 'r') as private_config_yaml:
                    private_config = yaml.load(private_config_yaml)
            except yaml.YAMLError as yaml_err:
                raise Failure('{} occurred during config initialization.'.format(yaml_err))
            Configuration.__instance._config = Config(public_config, private_config)
        return Configuration.__instance._config
