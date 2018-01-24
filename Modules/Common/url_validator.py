import requests

from Modules.Common.checker import Failure
from Modules.Common.helper import LogClass
from Modules.Common.logger import Logger


class URLValidator:
    def __init__(self):
        self.logger = Logger(name='URL Validator', log_name='url_validator', log_to_file=True,
                             log_script_information=True, log_class=LogClass.Info)

    def validate_url(self, url, use_head=False):
        self.logger.log_string(LogClass.Info, 'Validation URL {}'.format(url))
        try:
            if not use_head:
                resp = requests.get(url)
            else:
                resp = requests.head(url)
            log_string = 'Status code: {}\tText: {}\tHeaders: {}\t'.format(resp.status_code, resp.text, resp.headers)
            self.logger.log_string(LogClass.Trace, 'Got response from {}: {}'.format(url, log_string))
            if resp.status_code / 100 < 4:
                self.logger.log_string(LogClass.Info, 'URL {} valid.'.format(url))
                return True
            else:
                self.logger.log_string(LogClass.Info, 'URL {} invalid.'.format(url))
                return False
        except BaseException as e:
            error_msg = 'Error {} occurred during URL {} validation.'.format(e, url)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
