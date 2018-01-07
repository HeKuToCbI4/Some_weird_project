import datetime

import telebot

import telegrambot.config as config
import telegrambot.weather_api as weather_api
from Modules.helper import LogClass
from Modules.logger import Logger

bot = telebot.TeleBot(config.token)
bot_logger = Logger(name='Bot logger', log_class=LogClass.Info, log_to_file=True, log_script_information=True,
                    log_name='bot_log_{}.txt'.format(
                        datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')))


@bot.message_handler(content_types=['text'])
def handle_messages(message):
    try:
        bot_logger.log_string(LogClass.Info, f'Got message from {message.chat.id}: {message}')
        message_string = str(message.text).lower()
        if message_string.__contains__('погода'):
            city = message_string.split(' ')[1]
            weather = weather_api.get_current_weather(weather_api.get_city_id(city))
            if weather is not None:
                message_to_send = 'Текуща погода: {}\nТемпература:{}\nМаксимальная температура: {}\nМинимальная температура: {}' \
                                  '\nДавление: {}\nВлажность: {}'.format(
                    weather.description, weather.temp, weather.temp_max, weather.temp_min, weather.pressure,
                    weather.humidity)
            else:
                message_to_send = 'Возникла ошибка, соси хуй!'
        else:
            message_to_send = message.text
        bot.send_message(message.chat.id, message_to_send)
        log_string = 'Sent message: {message_to_send}'.format(
            message_to_send=message_to_send)
        bot_logger.log_string(LogClass.Info, log_string)

    except Exception as e:
        bot_logger.log_string(LogClass.Exception, f'{e} occured.')


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
