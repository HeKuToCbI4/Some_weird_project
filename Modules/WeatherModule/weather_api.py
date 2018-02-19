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
        # Get current weather in the city
        self._logger.log_string(LogClass.Info, 'Getting current weather in {}'.format(city))
        observation = self._owm_api.weather_at_place(city)
        weather = observation.get_weather()
        sunrise = self._tz.localize(datetime.datetime.fromtimestamp(weather.get_sunrise_time())).strftime('%H:%M:%S %Z')
        sunset = self._tz.localize(datetime.datetime.fromtimestamp(weather.get_sunset_time())).strftime('%H:%M:%S %Z')
        result = OneDayForecast(weather.get_status(), weather.get_temperature('celsius')['temp'],
                                weather.get_wind()['speed'], weather.get_pressure()['press'] * 750.1 // 1000,
                                weather.get_humidity(),
                                sunrise, sunset)
        self._logger.log_string(LogClass.Info, 'Successfully got current weather in {}'.format(city))
        return result

    def get_five_day_forecast_in_city(self, city):
        # Returns forecast object which contains information for five corresponding days in %city% with three hours
        # interval.
        self._logger.log_string(LogClass.Info, 'Getting three-hours forecast in {}'.format(city))
        forecast = self._owm_api.three_hours_forecast(city).get_forecast()
        self._logger.log_string(LogClass.Info,
                                'Successfully got forecast for five corresponding days in {}'.format(city))
        return forecast


if __name__ == '__main__':
    wp = OWMProvider()
    res = wp.get_five_day_forecast_in_city('samara')
