import collections
import datetime

import pyowm
import pytz

from Modules.Common import logger
from Modules.Common.helper import LogClass, Configuration

OneDayForecast = collections.namedtuple('OneDayForecast',
                                        'description temp wind pressure humidity sunrise sunset')
api_key = Configuration().cfg.private['open_weather']['api_key']


class OWMProvider:
    def __init__(self, timezone='Europe/Moscow'):
        self._logger = logger.Logger(name='WeatherLogger', log_class=LogClass.Info, log_script_information=True,
                                     log_to_file=True, log_name='weather_log.txt')
        self._owm_api = pyowm.OWM(API_key=api_key, language='ru')
        self._tz = pytz.timezone(timezone)

    def get_current_weather_in_city(self, city):
        observation = self._owm_api.weather_at_place(city)
        weather = observation.get_weather()
        sunrise = self._tz.localize(datetime.datetime.fromtimestamp(weather.get_sunrise_time())).strftime('%H:%M:%S %Z')
        sunset = self._tz.localize(datetime.datetime.fromtimestamp(weather.get_sunset_time())).strftime('%H:%M:%S %Z')
        result = OneDayForecast(weather.get_status(), weather.get_temperature('celsius')['temp'],
                                weather.get_wind()['speed'], weather.get_pressure()['press'], weather.get_humidity(),
                                sunrise, sunset)
        return result


if __name__ == '__main__':
    wp = OWMProvider()
    wp.get_current_weather_in_city('samara')
