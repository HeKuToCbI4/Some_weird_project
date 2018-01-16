import datetime

import vk_api

from Configurations.vk_module_config import login, password
from Modules.Common.checker import Failure
from Modules.Common.helper import LogClass
from Modules.Common.logger import Logger


class VkModule:
    def __init__(self, custom_login=None, custom_password=None):
        self.logger = Logger(name='VK Logger')
        self._password = password if custom_password is None else custom_password
        self._login = login if custom_login is None else custom_login
        self.logger.log_string(LogClass.Trace,
                               "Attempting to perform authentication with {} - {} credentials".format(self._login,
                                                                                                      self._password))
        self._authenticate(self._login, self._password)
        self.logger.log_string(LogClass.Info,
                               "Authentication with {} - {} successful.".format(self._login, self._password))

    def _auth_handler(self):
        # При двухфакторной аутентификации вызывается эта функция.
        # Код двухфакторной аутентификации
        self.logger.log_string(LogClass.Warning, "Two-factor authentication confirmation required!")
        key = input("Enter authentication code: ")
        # Если: True - сохранить, False - не сохранять.
        remember_device = True
        return key, remember_device

    def _authenticate(self, login, password):
        vk_session = vk_api.VkApi(login=login, password=password, auth_handler=self._auth_handler)
        try:
            vk_session.auth()
        except vk_api.AuthError as e:
            self.logger.log_string(LogClass.Exception,
                                   "Exception {} occurred during authentication in VK with {} - {}.".format(e,
                                                                                                            self._login,
                                                                                                            self._password))
        self.api = vk_session.get_api()


