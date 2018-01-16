import datetime
from threading import Thread, Event
from time import sleep

import telebot

import telegrambot.config as config
import telegrambot.weather_api as weather_api
from Modules.Common.checker import Failure
from Modules.Common.helper import LogClass
from Modules.Common.logger import Logger
from Modules.VkModule.vk_module import VkModule


class TelegramBot:
    def __init__(self):
        self.bot = telebot.TeleBot(config.token)
        self.bot_logger = Logger(name='Bot logger', log_class=LogClass.Info, log_to_file=True,
                                 log_script_information=True,
                                 log_name='bot_log.txt')
        self.vk = VkModule()
        self.monitor_posts = {}

        @self.bot.message_handler(commands=['weather'])
        def handle_weather(message):
            try:
                self.bot_logger.log_string(LogClass.Info, f'Got message from {message.chat.id}: {message}')
                message_string = str(message.text).lower()
                city = message_string.split(' ')[1]
                weather = weather_api.get_current_weather(weather_api.get_city_id(city))
                if weather is not None:
                    message_to_send = 'Текуща погода: {}\nТемпература:{}\nМаксимальная температура: {}\nМинимальная температура: {}' \
                                      '\nДавление: {}\nВлажность: {}'.format(
                        weather.description, weather.temp, weather.temp_max, weather.temp_min, weather.pressure,
                        weather.humidity)
                else:
                    message_to_send = 'Возникла ошибка, соси хуй!'
                self.bot.send_message(message.chat.id, message_to_send)
                log_string = 'Sent message: {message_to_send}'.format(message_to_send=message.text)
                self.bot_logger.log_string(LogClass.Info, log_string)
            except BaseException as e:
                self.bot_logger.log_string(LogClass.Exception, 'Возникла ошибка при обработке погоды'.format(e))

        @self.bot.message_handler(commands=['monitor', 'off_monitor'])
        def handle_monitoring(message):
            try:
                self.bot_logger.log_string(LogClass.Info, f'Got message from {message.chat.id}: {message}')
                message_string = str(message.text).lower()
                try:
                    target = message_string.split(' ')[1]
                except BaseException:
                    message_to_send = 'Используйте формат /команда домен\nДомен-короткое имя страницы - цели.'
                    self.bot.send_message(message.chat.id, message_to_send)
                    raise Failure('Невозможно получить домен из сообщения {}'.format(message.text))
                if message_string.__contains__('/off_monitor'):
                    self.stop_monitoring_posts(target, message.chat.id)
                    message_to_send = 'Прекращён мониторинг постов со страницы {}'.format(target)
                else:
                    self.start_last_wall_posts_monitoring(target, message.chat.id)
                    message_to_send = 'Начинаем мониторинг постов в {}\nПоследние 5 постов:\n'.format(target)
                self.bot.send_message(message.chat.id, message_to_send)
                log_string = 'Sent message: {message_to_send}'.format(message_to_send=message_to_send)
                self.bot_logger.log_string(LogClass.Info, log_string)
            except BaseException as e:
                self.bot_logger.log_string(LogClass.Exception, f'{e} occurred.')

        @self.bot.message_handler(content_types=['text'])
        def handle_messages(message):
            self.bot_logger.log_string(LogClass.Trace, 'Got message at {}: {}'.format(message.chat.id, message.text))
            # self.bot.send_message(message.chat.id, message.text)
            # log_string = 'Sent message: {message_to_send}'.format(message_to_send=message.text)
            # self.bot_logger.log_string(LogClass.Info, log_string)

    def monitor_wall_posts(self, domain, chat_id):
        try:
            last_posts_ids = []
            while self.monitor_posts[(domain, chat_id)].isSet():
                five_last_posts = self.vk.get_n_last_wall_posts(domain=domain, count=5)
                for post in five_last_posts:
                    if not post['id'] in last_posts_ids:
                        self.bot.send_message(chat_id, "Новый пост на странице {}:\n{}".format(domain, post['text']))
                        last_posts_ids.append(post['id'])
                sleep(60)
                if len(last_posts_ids) > 50:
                    last_posts_ids = last_posts_ids[:50]
        except:
            self.monitor_posts.pop((domain, chat_id))

    def start_last_wall_posts_monitoring(self, domain, chat_id):
        if not (domain, chat_id) in self.monitor_posts.keys():
            self.monitor_posts[(domain, chat_id)] = Event()
        if not self.monitor_posts[(domain, chat_id)].isSet():
            self.monitor_posts[(domain, chat_id)].set()
            t = Thread(target=self.monitor_wall_posts, args=(domain, chat_id))
            t.setDaemon(True)
            t.start()

    def stop_monitoring_posts(self, domain, chat_id):
        self.monitor_posts[(domain, chat_id)].clear()

    def start_bot(self):
        self.bot.polling(none_stop=True)

    def stop_bot(self):
        self.bot.stop_polling()


def main():
    bot = TelegramBot()
    bot.start_bot()


if __name__ == '__main__':
    main()
