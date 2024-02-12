# 2019_CSSE1001_ASSIGNMENT_2
My second produced Python solution.

Overview

They are weather_data.py, prediction.py and event_decision.py. Each file defines a set of classes, which are described below. You will need to implement parts, or all, of the classes in the prediction.py and event_decision.py files.
The file, weather_data.py, contains the WeatherData and WeatherDataItem classes. WeatherData represents all the weather data that is loaded from the data file. WeatherDataItem represents weather data for a single day. It provides methods to access this data.
The prediction.py file defines the super class WeatherPrediction. It defines a set of methods that you need to override in subclasses that you implement for the assignment. An example of doing this is provided by the YesterdaysWeather subclass. You need to implement the SimplePrediction and SophisticatedPredication subclasses.
The file, event_decision.py, provides a description of the EventDecision class. It uses data about the event to determine if aspects of the weather would impact on the event. You will need to implement the __init__ and advisability methods. The advisability method determines how advisable it is to continue with the event, based on the weather prediction. Two other classes defined in this file are Event and UserInteraction. The Event class represents the data about an event and defines a set of methods that you will need to implement. The UserInteraction class provides methods that allow the program to interact with the user. It defines a set of methods that you will need to implement. Two of these methods, get_prediction_model and output_advisability, are partially implemented with some example ideas that you may use in your solution.

![image](https://github.com/generalfos/2019_CSSE1001_ASSIGNMENT_2/assets/52812748/30b23119-e870-4128-ae96-6a1e5c202d8e)
