"""
    Simple application to help make decisions about the suitability of the
    weather for a planned event. Second assignment for CSSE1001/7030.

    Event: Represents details about an event that may be influenced by weather.
    EventDecider: Determines if predicted weather will impact on a planned event.
    UserInteraction: Simple textual interface to drive program.
"""

__author__ = "Joel Foster - 45820384"
__email__ = "joel.foster@uqconnect.edu.au"

from weather_data import WeatherData
from prediction import (WeatherPrediction, YesterdaysWeather, SimplePrediction,
SophisticatedPrediction)

class Event(object):
    """ Stores data related to the users event. """
    
    def __init__(self, name, outdoors, cover_available, time):
        """Initialises an instance of the event object

        Parameters:
            name(str): The name of the event.
            outdoors(bool): True if the event is outdoors.
            cover_available(bool): True if cover is available.
            time(int): The closest hour to the starting time of the event.

        Preconditions:
            0 <= time < 24 
        """
        self._name = name
        self._outdoors = outdoors
        self._cover = cover_available
        self._time = time

    def get_name(self):
        """(str) The name of the event."""
        return self._name

    def get_time(self):
        """(int) The time of the event."""
        return self._time

    def get_outdoors(self):
        """(bool) True if the event is outdoors, false otherwise."""
        return self._outdoors

    def get_cover_available(self):
        """(bool) True if cover is available, false otherwise."""
        return self._cover

    def __str__(self):
        """(str) String representation of the event object."""
        return f'Event({self._name} @ {self._time}, {self._outdoors}, {self._cover})'
    


class EventDecision(object):
    """Uses event details to decide if predicted weather suits an event."""

    def __init__(self, event, prediction_model):
        """
        Parameters:
            event (Event): The event to determine its suitability.
            prediction_model (WeatherPrediction): Specific prediction model.
                           An object of a subclass of WeatherPrediction used 
                           to predict the weather for the event.
        """
        self._event = event
        self._prediction_model = prediction_model
        

    def _temperature_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted temperature

        Return:
            (float) Temperature Factor
        """
        humidity_factor = 0
        if self._prediction_model.humidity() > 70:
            humidity_factor = self._prediction_model.humidity() / 20
        
        if self._prediction_model.high_temperature() >= 0:
            high_temp = self._prediction_model.high_temperature() + humidity_factor
        elif self._prediction_model.high_temperature() < 0:
            high_temp = self._prediction_model.high_temperature() - humidity_factor
        if self._prediction_model.low_temperature() >= 0:
            low_temp = self._prediction_model.low_temperature() + humidity_factor
        elif self._prediction_model.low_temperature() < 0:
            low_temp = self._prediction_model.low_temperature() - humidity_factor

        temp_factor = 0
        method_1 = False
        method_2 = False
        
        if 6 <= self._event._time <= 19:
            if self._event.get_outdoors():
                if high_temp >= 30:
                    temp_factor = (high_temp/(-5)) + 6
                    method_1 = True

        if high_temp >= 45:
            temp_factor = (high_temp/(-5)) + 6
            method_2 = True

        if 0 <= self._event._time <= 5 or 20 <= self._event._time <= 23:
            if low_temp < 5 and high_temp < 45:
                temp_factor = (low_temp/5) - 1.1

        if low_temp > 15 and high_temp < 30:
            temp_factor = (high_temp - low_temp)/5

        # Step 3
        if temp_factor < 0 and (method_1 or method_2):
            if self._event.get_cover_available():
                temp_factor += 1
            if 3 < self._prediction_model.wind_speed() < 10:
                temp_factor += 1
            if self._prediction_model.cloud_cover() > 4:
                temp_factor += 1
        return temp_factor
    
    def _rain_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted rainfall

        Return:
            (float) Rain Factor
        """
        if self._prediction_model.chance_of_rain() < 20:
            rain_factor = (self._prediction_model.chance_of_rain()/(-5))+4
        elif self._prediction_model.chance_of_rain() > 50:
            rain_factor = (self._prediction_model.chance_of_rain()/(-20))+1
        else:
            rain_factor = 0

        if self._event.get_cover_available():
            if self._event.get_outdoors():
                if self._prediction_model.wind_speed() < 5:
                    rain_factor += 1
                    
        if rain_factor < 2 and self._prediction_model.wind_speed() > 15:
            rain_factor += self._prediction_model.wind_speed()/(-15)
        if rain_factor < -9:
            rain_factor = -9
        return rain_factor            

    def advisability(self):
        """Determine how advisable it is to continue with the planned event.

        Return:
            (float) Value in range of -5 to +5,
                    -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        advisability = self._temperature_factor() + self._rain_factor()
        
        if advisability < -5:
            advisability = -5
        if advisability > 5:
            advisability = 5
        
        return advisability


class UserInteraction(object):
    """Simple textual interface to drive program."""

    def __init__(self):
        """ Initialises the user interaction object """
        self._event = None
        self._prediction_model = None

    def get_event_details(self):
        """Prompt the user to enter details for an event.

        Return:
            (Event): An Event object containing the event details.
        """
        time_invalid = True
        outdoors_invalid = True
        shelter_invalid = True
        
        name = input('What is the name of your event? ')
        
        outdoors = input('Is your event outdoors? ').lower()

        # Validate user input.
        while outdoors_invalid:
            if outdoors == 'yes' or outdoors == 'y':
                outdoors = True
                outdoors_invalid = False
            elif outdoors == 'no' or outdoors == 'n':
                outdoors = False
                outdoors_invalid = False
            else:
                print('That is an invalid input. Please try again.')
                outdoors = input('Is your event outdoors? ').lower()
        
        shelter = input("Is there covered shelter? ").lower()

        while shelter_invalid:
            if shelter == 'yes' or shelter == 'y':
                shelter = True
                shelter_invalid = False
            elif shelter == 'no' or shelter == 'n':
                shelter = False
                shelter_invalid = False
            else:
                print('That is an invalid input. Please try again.')
                shelter = input("Is there covered shelter? ").lower()
        
        time = input('At what hour will your event be starting? ')

        while time_invalid:
            try:
                time = int(time)
                if 0 <= time < 24:
                    time_invalid = False
                else:
                    print('That is an invalid time. Please try again.')
                    time = input('At what hour will your event be starting? ')
            except ValueError:
                print('That is an invalid time. Please try again.')
                time = input('At what hour will your event be starting? ')

        self._event = Event(name, outdoors, shelter, time)
        return self._event
        
    def _validate_model_choice(self, model_choice):
        """ Validates user input against available prediction models.

        Parameter:
            model_choice (str): User input for get_prediction_model().

        Return:
            (bool) True iff the requested model exists. 
        """
        if model_choice in ['1', '2', '3']:
            return True
        else:
            return False
        
    def get_prediction_model(self, weather_data):
        """Prompt the user to select the model for predicting the weather.

        Parameter:
            weather_data (WeatherData): Data used for predicting the weather.

        Return:
            (WeatherPrediction): Object of the selected prediction model.
        """
        days = None
        print("Select the weather prediction model you wish to use:")
        print("  1) Yesterday's weather.")
        print("  2) Simple Prediction.")
        print("  3) Sophisticated Prediction.")
        model_choice = input("> ")
        while days == None:
            if self._validate_model_choice(model_choice):
                if model_choice == '1' :
                    days = 1
                    self._prediction_model = YesterdaysWeather(weather_data)
                elif model_choice == '2' :
                    print("How many days of data should be used in the prediction?")
                    days = input("> ")
                    self._prediction_model = SimplePrediction(weather_data, days)
                elif model_choice == '3' :
                    print("How many days of data should be used in the prediction?")
                    days = input("> ")
                    self._prediction_model = SophisticatedPrediction(weather_data, days)
            else:
                print("That is not a valid model choice. Please try again.")
                model_choice = input("> ")

        return self._prediction_model

    def output_advisability(self, impact):
        """Output how advisable it is to go ahead with the event.

        Parameter:
            impact (float): Impact of the weather on the event.
                            -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        print("Based on the", type(self._prediction_model).__name__, "model",
              "the advisability of continuing", self._event.get_name(), "is",
              impact)
        
        

    def another_check(self):
        """Ask user if they want to check using another prediction model.

        Return:
            (bool): True if user wants to check using another prediction model.
        """
        user_input = input("Would you like to try a different \
weather prediction model? ").lower()
        while True:
            if user_input in ['y', 'yes']:
                return True
            elif user_input in ['n', 'no']:
                return False
            else:
                print('That is an invalid input. Please try again.')
                user_input = input("Would you like to try a different \
weather prediction model? ").lower()


def main():
    """Main application's starting point."""
    check_again = True
    weather_data = WeatherData()
    weather_data.load("weather_data.csv")
    user_interface = UserInteraction()

    print("Let's determine how suitable your event is for the predicted weather.")
    event = user_interface.get_event_details()

    while check_again:
        prediction_model = user_interface.get_prediction_model(weather_data)
        decision = EventDecision(event, prediction_model)
        impact = decision.advisability()
        user_interface.output_advisability(impact)
        check_again = user_interface.another_check()


if __name__ == "__main__":
    main()
