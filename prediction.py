"""
    Prediction model classes used in the second assignment for CSSE1001/7030.

    WeatherPrediction: Defines the super class for all weather prediction models.
    YesterdaysWeather: Predict weather to be similar to yesterday's weather.
    SimplePrediction: Provide a rough approximation of the weather
                      using the weather of the past n days.
    SophisticatedPrediction: Accurately predict weather using the weather
                             of the past n days.
"""

__author__ = "Joel Foster - 45820384"
__email__ = "joel.foster@uqconnect.edu.au"

from weather_data import WeatherData


class WeatherPrediction(object):
    """Superclass for all of the different weather prediction models."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        self._weather_data = weather_data

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        raise NotImplementedError

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        raise NotImplementedError

    def high_temperature(self):
        """(float) Expected high temperature."""
        raise NotImplementedError

    def low_temperature(self):
        """(float) Expected low temperature."""
        raise NotImplementedError

    def humidity(self):
        """(int) Expected humidity."""
        raise NotImplementedError

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        raise NotImplementedError

    def wind_speed(self):
        """(int) Expected average wind speed."""
        raise NotImplementedError


class YesterdaysWeather(WeatherPrediction):
    """Simple prediction model, based on yesterday's weather."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        self._yesterdays_weather = self._weather_data.get_data(1)
        self._yesterdays_weather = self._yesterdays_weather[0]

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        return 1

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        # Amount of yesterday's rain indicating chance of it occurring.
        NO_RAIN = 0.1
        LITTLE_RAIN = 3
        SOME_RAIN = 8
        # Chance of rain occurring.
        NONE = 0
        MILD = 40
        PROBABLE = 75
        LIKELY = 90

        if self._yesterdays_weather.get_rainfall() < NO_RAIN:
            chance_of_rain = NONE
        elif self._yesterdays_weather.get_rainfall() < LITTLE_RAIN:
            chance_of_rain = MILD
        elif self._yesterdays_weather.get_rainfall() < SOME_RAIN:
            chance_of_rain = PROBABLE
        else:
            chance_of_rain = LIKELY

        return chance_of_rain

    def high_temperature(self):
        """(float) Expected high temperature."""
        return self._yesterdays_weather.get_high_temperature()

    def low_temperature(self):
        """(float) Expected low temperature."""
        return self._yesterdays_weather.get_low_temperature()

    def humidity(self):
        """(int) Expected humidity."""
        return self._yesterdays_weather.get_humidity()

    def wind_speed(self):
        """(int) Expected average wind speed."""
        return self._yesterdays_weather.get_average_wind_speed()

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        return self._yesterdays_weather.get_cloud_cover()

class SimplePrediction(WeatherPrediction):
    """ Simple prediction model based on 'n' days weather """
    
    def __init__(self, weather_data, days):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.
            days (str): Number of days of data to be used.

        Pre-condition:
            weather_data.size() > 0
            days > 0
        """
        super().__init__(weather_data)
        # Determines whether there is enough data to satify the users request.
        if int(days) > self._weather_data.size():
            self._days = self._weather_data.size()
        else:
            self._days = int(days)
        self._event_weather = self._weather_data.get_data(self._days)
        self._event_weather = self._event_weather[::-1]
        
    def get_number_days(self):
        """(int) Number of days of weather data used by the prediction model."""
        return len(self._event_weather)
    
    def chance_of_rain(self):
        """(int) Average rainfall over the past n days."""
        total_rainfall = 0
        for day in self._event_weather:
            total_rainfall += day.get_rainfall()
        average_rainfall = total_rainfall / self.get_number_days()
        result = (9 * average_rainfall).__round__()
        if result > 100:
            result = 100
        return result

    def high_temperature(self):
        """(float) Highest temperature of the past n days."""
        high_temperatures = []
        for day in self._event_weather:
            high_temperatures.append(day.get_high_temperature())
        return max(high_temperatures)

    def low_temperature(self):
        """(float) Lowest temperature of the past n days."""
        low_temperatures = []
        for day in self._event_weather:
            low_temperatures.append(day.get_low_temperature())
        return min(low_temperatures)

    def humidity(self):
        """(int) Average humidity over the past n days."""
        total_humidity = 0
        for day in self._event_weather:
            total_humidity += day.get_humidity()
        average_humidity = total_humidity / self.get_number_days()
        return (average_humidity).__round__()

    def cloud_cover(self):
        """(int) Average cloud cover over the past n days."""
        total_cloud_cover = 0
        for day in self._event_weather:
            total_cloud_cover += day.get_cloud_cover()
        average_cloud_cover = total_cloud_cover / self.get_number_days()
        return (average_cloud_cover).__round__()

    def wind_speed(self):
        """(int) Average wind speed over the past n days."""
        total_wind_speed = 0
        for day in self._event_weather:
            total_wind_speed += day.get_average_wind_speed()
        average_wind_speed = total_wind_speed / self.get_number_days()
        return (average_wind_speed).__round__()

class SophisticatedPrediction(WeatherPrediction):
    """ Sophisticated prediction model based on the previous'n' days of weather
        data.
    """

    def __init__(self, weather_data, days):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.
            days (str): Number of days of data to be used.

        Pre-condition:
            weather_data.size() > 0
            days > 0
        """
        super().__init__(weather_data)
        if int(days) > self._weather_data.size():
            self._days = self._weather_data.size()
        else:
            self._days = int(days)
        self._event_weather = self._weather_data.get_data(self._days)
        self._event_weather = self._event_weather[::-1]

    def get_number_days(self):
        """(int) Number of days used by the prediction model."""
        return len(self._event_weather)

    def air_pressure(self):
        """ (float) Average air pressure over the past n days."""
        total_air_pressure = 0
        for day in self._event_weather:
            total_air_pressure += day.get_air_pressure()
        average_air_pressure = total_air_pressure / self.get_number_days()
        return average_air_pressure
    
    def chance_of_rain(self):
        """(int) Average rainfall over the past n days."""
        total_rainfall = 0
        East = False
        for day in self._event_weather:
            total_rainfall += day.get_rainfall()
        average_rainfall = total_rainfall / self.get_number_days()
        
        if self._event_weather[0].get_air_pressure() < self.air_pressure():
            average_rainfall *= 10
        elif self._event_weather[0].get_air_pressure() >= self.air_pressure():
            average_rainfall *= 7

        for direction in self._event_weather[0].get_wind_direction():
            if direction == 'E':
                East = True
                break

        if East == True:
            average_rainfall *= 1.2
        if average_rainfall > 100:
            average_rainfall = 100
        return (average_rainfall).__round__()
    
    def high_temperature(self):
        """(float) Average high temperature over the past n days."""
        total_high_temperature = 0
        for day in self._event_weather:
            total_high_temperature += day.get_high_temperature()
        average_high_temperature = total_high_temperature / self.get_number_days()

        if self._event_weather[0].get_air_pressure() > self.air_pressure():
            average_high_temperature += 2
        return average_high_temperature

    def low_temperature(self):
        """(float) Average low temperature over the past n days."""
        total_low_temperature = 0
        for day in self._event_weather:
            total_low_temperature += day.get_low_temperature()
        average_low_temperature = total_low_temperature / self.get_number_days()

        if self._event_weather[0].get_air_pressure() < self.air_pressure():
            average_low_temperature -= 2
        return average_low_temperature

    def humidity(self):
        """(float) Average humidity over the past n days."""
        total_humidity = 0
        for day in self._event_weather:
            total_humidity += day.get_humidity()
        average_humidity = total_humidity / self.get_number_days()

        if self._event_weather[0].get_air_pressure() < self.air_pressure():
            average_humidity += 15
        elif self._event_weather[0].get_air_pressure() > self.air_pressure():
            average_humidity -= 15

        if average_humidity < 0:
            average_humidity = 0
        if average_humidity > 100:
            average_humidity = 100

        return (average_humidity).__round__()

    def cloud_cover(self):
        """(float) Average cloud cover over the past n days."""
        total_cloud_cover = 0
        for day in self._event_weather:
            total_cloud_cover += day.get_cloud_cover()
        average_cloud_cover = total_cloud_cover / self.get_number_days()

        if self._event_weather[0].get_air_pressure() < self.air_pressure():
            average_cloud_cover += 2

        if average_cloud_cover > 9:
            average_cloud_cover = 9
        return (average_cloud_cover).__round__()

    def wind_speed(self):
        """(int) Average wind speed over the past n days."""
        total_wind_speed = 0
        for day in self._event_weather:
            total_wind_speed += day.get_average_wind_speed()
        average_wind_speed = total_wind_speed / self.get_number_days()
        
        if self._event_weather[0].get_maximum_wind_speed() > (4 * average_wind_speed):
            average_wind_speed *= 1.2
        return (average_wind_speed).__round__()

if __name__ == "__main__":
    print("This module provides the weather prediction models",
          "and is not meant to be executed on its own.")



