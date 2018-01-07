import collections
import datetime

import requests

from Modules import logger
from Modules.helper import LogClass

OneDayForecast = collections.namedtuple('OneDayForecast',
                                        'description temp temp_min temp_max pressure humidity ')

api_key = 'eb63aec54892c8f55cdeccb05fd792fd'

weather_logger = logger.Logger(name='WeatherLogger', log_class=LogClass.Info, log_script_information=True,
                               log_to_file=True, log_name='weather_log_{}.txt'.format(
        datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')))


def get_city_id(city):
    city += ',RU'
    try:
        result = requests.get("http://api.openweathermap.org/data/2.5/find",
                              params={'q': city, 'type': 'like', 'units': 'metric', 'APPID': api_key})

        data = result.json()

        city_id = data['list'][0]['id']
    except Exception as e:
        weather_logger.log_string(LogClass.Exception, f'Exception {e} occured.')
        return None
    return city_id


def get_current_weather(city_id):
    if city_id is not None:
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                               params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': api_key})
            data = res.json()
            result = OneDayForecast(data['weather'][0]['description'], data['main']['temp'], data['main']['temp_min'],
                                    data['main']['temp_max'], data['main']['pressure'], data['main']['humidity'])
            weather_logger.log_string(LogClass.Info, f'Got response: {data}')

        except Exception as e:
            weather_logger.log_string(LogClass.Exception, f"Exception (weather): {e}")
            return None
        return result
    return None
