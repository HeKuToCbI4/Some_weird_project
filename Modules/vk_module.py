import vk_api

from Configurations.vk_module_config import login, password
from Modules.checker import Failure
from Modules.helper import LogClass
from Modules.logger import Logger


class VkModule:
    def __init__(self, custom_login=None, custom_password=None):
        self.logger = Logger(name='Vk logger', log_script_information=True, log_to_file=True, log_name='vk_module_log')
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

    def get_last_wall_post(self, owner_id=0, domain=None, **kwargs):
        return self.get_n_last_wall_posts(owner_id, domain, 1, **kwargs)[0]

    def get_n_last_wall_posts(self, owner_id=0, domain=None, count=1, **kwargs):
        destination = 'destination {}, with {}'.format(owner_id if domain is None else domain, kwargs.keys())
        self.logger.log_string(LogClass.Info, "Sending 'get wall posts' request to {}".format(destination))
        if domain is None:
            response = self.api.wall.get(owner_id=owner_id, count=count, **kwargs)
        else:
            response = self.api.wall.get(domain=domain, count=count, **kwargs)
        self.logger.log_string(LogClass.Info, "Got response from {}: {}".format(destination, response))
        if response['items']:
            return response['items']
        else:
            message = 'Something gone wrong during request to {}.'.format(destination)
            self.logger.log_string(LogClass.Exception, message)
            raise Failure(message)


if __name__ == '__main__':
    vk = VkModule()
    response = vk.get_n_last_wall_posts(domain='nycoffee_samara', count=5)
    print(response)
