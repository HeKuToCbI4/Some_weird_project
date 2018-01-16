import smtplib

from Configurations.google_mail_config import login, password
from Modules.Common.checker import Failure
from Modules.Common.helper import Configuration
from Modules.Common.helper import LogClass
from Modules.Common.logger import Logger

cfg = Configuration().cfg
smtp_config = cfg['smtp_servers']


class EMailProvider:
    def __init__(self, server=None):
        default_server = smtp_config['servers']['default_server']
        connection_timeout = smtp_config['connection_timeout']
        self._server_to_connect_to = server if server is not None else default_server
        self.logger = Logger(name='EmailProvider {}'.format(self._server_to_connect_to), log_class=LogClass.Info,
                             log_script_information=True,
                             log_to_file=True, log_name='EmailProvider')
        self.logger.log_string(LogClass.Info, 'Attempting to connect to {}'.format(self._server_to_connect_to))
        try:
            self._smtp = smtplib.SMTP(host=self._server_to_connect_to['address'],
                                      port=self._server_to_connect_to['port'],
                                      timeout=connection_timeout)
            self._smtp.ehlo()
        except smtplib.SMTPException:
            error_msg = 'Failed to establish connection to {} in {} seconds.'.format(self._server_to_connect_to,
                                                                                     connection_timeout)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        self.logger.log_string(LogClass.Info, 'Starting TLS encryption')
        response, reply = self._smtp.starttls()
        self.logger.log_string(LogClass.Info, 'Got {}: {} response from server.'.format(response, reply))
        if 220 != response:
            error_msg = 'Failed to start TLS on {}'.format(self._server_to_connect_to)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)

    def authorize(self, email, password):
        self.logger.log_string(LogClass.Info,
                               'Attempting login to {} for user {}'.format(self._server_to_connect_to, email))
        try:
            self._smtp.login(user=email, password=password)
        except smtplib.SMTPException:
            error_msg = 'Failed to authorize to {} for user {}'.format(self._server_to_connect_to, email)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        self.logger.log_string(LogClass.Info, 'Authorized {} on {}'.format(email, self._server_to_connect_to))

    def send_email(self, from_addr, to_addr, message, subject=None):
        if subject is not None:
            message_to_send = 'Subject: {}\n\n{}'.format(subject, message)
        else:
            message_to_send = message
        self.logger.log_string(LogClass.Info,
                               'Attempting to send mail: {} from {} to {} on {}'.format(message_to_send, from_addr,
                                                                                        to_addr,
                                                                                        self._server_to_connect_to))
        try:
            self._smtp.sendmail(from_addr, to_addr, message_to_send.encode())
        except smtplib.SMTPException:
            error_msg = 'Failed to send message from {} to {} on {}'.format(from_addr, to_addr,
                                                                            self._server_to_connect_to)
            self.logger.log_string(LogClass.Exception, error_msg)
            raise Failure(error_msg)
        self.logger.log_string(LogClass.Info, 'Message from {} to {} sent on {}'.format(from_addr, to_addr,
                                                                                        self._server_to_connect_to))

    def stop(self):
        self._smtp.quit()


if __name__ == '__main__':
    emp = EMailProvider()
    emp.authorize(login, password)
    emp.send_email(from_addr=login, to_addr='leonov2424@mail.ru',
                   message='Subject: Винтовка это праздник\n\nВсё летит в пизду')
    emp.stop()
