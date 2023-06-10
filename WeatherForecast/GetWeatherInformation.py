from enum import Enum
from pyowm import OWM
from WeatherForecast import WeatherPoint

from WeatherForecast.WeatherPointInformation import getWeatherPointInformation

class GetWeatherInformation():
    def __init__(self,apiKey:str) -> None:
        self.apiKey = apiKey

        owm =OWM(apiKey)
        self.owm_manager = owm.weather_manager()

    def getWeather(self,point:WeatherPoint.WeatherPoint) :
        pointInformation = getWeatherPointInformation(point)
        return self.owm_manager.one_call(pointInformation.lat,pointInformation.lon,units="imperial")