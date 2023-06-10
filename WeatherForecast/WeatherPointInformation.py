
from WeatherForecast import WeatherPoint


class PointInformation():

    def __init__(self,lat:float,lon:float):
        self.lat = lat
        self.lon = lon

def getWeatherPointInformation(point:WeatherPoint.WeatherPoint) -> PointInformation :
    if point == WeatherPoint.WeatherPoint.AKASHI:
        return PointInformation(34.6490479,134.9927312)
    elif point == WeatherPoint.WeatherPoint.Osaka:
        return PointInformation(34.7022887,135.4953509)
    elif point == WeatherPoint.WeatherPoint.KAKOGAWA:
        return PointInformation(34.767526,134.8396018)
    