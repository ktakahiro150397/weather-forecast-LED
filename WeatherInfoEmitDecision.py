from datetime import datetime, timezone, timedelta
import logging


class WeatherInfoEmitDecision():

    def __init__(self):

        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())
        self._logger.setLevel(logging.DEBUG)
        self._logger.propagate = True

        # 傘が必要な天気ID
        # https://openweathermap.org/weather-conditions
        self._umblleraRequiredWeatherId = [
            200,201,202,210,211,212,221,230,231,232,301,302,311,312,313,314,321,
            501,502,503,504,511,521,522,531,600,602,611,612,613,615,616,620,621,622,
            751,761,762,771
        ]

    def isBlink(self,weatherInfo) -> bool:
        
        # 必要なデータを取得する
        # .forecast_hourly.を参照する
        #.weather_code,
        # datetime.fromtimestamp(.ref_time, tz=timezone.utc).isoformat(' ', 'seconds')  + 9h
        check_data = [(elem.weather_code,
                       datetime.fromtimestamp(elem.ref_time, tz=timezone.utc) + timedelta(hours=9)) 
                       for elem in weatherInfo.forecast_hourly]
        
        # 今日日付のデータを取得
        check_data = [ elem for elem in check_data if elem[1].date() == datetime.now().date() ]

        # 中に傘が必要なweather_codeが存在すればTrueを返す
        return self._isUmbllela_Required([elem[0] for elem in check_data])

    def _isUmbllela_Required(self,weather_code: list) -> bool:
        common = list(set(weather_code) &  set(self._umblleraRequiredWeatherId))

        self._logger.debug("common:{}".common(weather_code))

        return len(common) > 0