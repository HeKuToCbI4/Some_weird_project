import vk_api

from Modules.Common.helper import Configuration
from Modules.Common.checker import Failure
from Modules.Common.helper import LogClass
from Modules.Common.logger import Logger

cfg = Configuration().cfg
vk_config = cfg.private['vk']
class VkModule:
    """Module used to provide access to Vk and return API"""
    def __init__(self, custom_login=None, custom_password=None, token=None, use_token=True):
        self.logger = Logger(name='VK Logger')
        self._password = vk_config['password'] if custom_password is None else custom_password
        self._login = vk_config['login'] if custom_login is None else custom_login
        self._token = token if token is not None else vk_config['api_key']
        self.logger.log_string(LogClass.Trace, "Attempting to perform authentication with {}".format(
            self._login if not use_token else 'token'))
        if use_token:
            self._authenticate(token=self._token)
        else:
            self._authenticate(self._login, self._password)
        self.logger.log_string(LogClass.Info,
                               "Authentication with {} successful.".format(self._login if not use_token else 'token'))

    def _auth_handler(self):
        # Called when two-factor auth is needed
        self.logger.log_string(LogClass.Warning, "Two-factor authentication confirmation required!")
        key = input("Enter authentication code: ")
        remember_device = True
        return key, remember_device

    def _authenticate(self, login=None, password=None, token=None):
        vk_session = vk_api.VkApi(login=login, password=password,
                                  auth_handler=self._auth_handler) if token is None else vk_api.VkApi(token=token)
        try:
            if token is None:
                vk_session.auth()
        except vk_api.AuthError as e:
            error_string = "Exception {} occurred during authentication in VK with {}.".format(e,
                                                                                               self._login if token is None else token)
            self.logger.log_string(LogClass.Exception, error_string)
            raise Failure(error_string)
        self.api = vk_session.get_api()


if __name__ == '__main__':
    vk = VkModule()
