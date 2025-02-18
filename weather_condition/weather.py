from dotenv import load_dotenv #type: ignore
from typing import Dict
import logging
import requests #type: ignore
import os 

from .dialog import DialogHandler
from .date_handler import DateHandler

# Load the .env file
load_dotenv()

# Access the keys
owm_key = os.getenv("OWM_KEY")

class Weather:
    """Weather class for interacting with weather data from OpenWeatherMap API."""
    
    def __init__(self):
        """Initialize the Weather class with necessary attributes."""
        self.owm_api_key = owm_key  # OpenWeatherMap API key
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"  # Base URL for weather data forecast 5 days
        self.city = None  # City for which to fetch the weather
        self.time = None  # Time range for weather data (e.g. today, tomorrow or the next 2 days)
        self.condition = None  # Weather condition (e.g. rain, snow, cloudy)
        self.temperature = None  # Temperature data (e.g. hot, cold, warm)
        self.wind_speed = None  # Wind speed data
        self.dialog_handler = DialogHandler() # Handler for dialog responses (the format of the response)
        self.date_handler = DateHandler() # Hanlder for setting and transforming the correct date
        
    def __fetch_weather_forecast_data(self):
        """Fetches weather forecast data from OpenWeatherMap API for a specified city.

        Makes an HTTP GET request to the OpenWeatherMap API using the provided city name
        and API key, and returns the response in JSON format.

        Returns:
            dict: JSON response from the OpenWeatherMap API containing weather forecast data.
        """

        # Define request parameters
        params = {
            "q": self.city,  # City name for which to fetch weather data
            "appid": self.owm_api_key,  # OpenWeatherMap API key
            "units": "metric"  # Use metric units for temperature
        }

        # Perform GET request to fetch data
        response = requests.get(self.base_url, params=params)

        # Return the JSON response
        return response.json()

    def __fetch_weather(self, time_range):
        """Fetches and formats weather data based on request parameters.

        Makes an HTTP GET request to the OpenWeatherMap API using the provided city name
        and API key, and formats the response into a human-readable format.

        Args:
            time_range (str): Time range for which to fetch weather data.

        Returns:
            str: Formatted weather data as a string.
        """
        if not self.city:
            return self.dialog_handler.handle_missing_city()  # Use DialogHandler for missing city
        logging.info(f"📡 Fetching weather for {self.city} at {self.time}")
        data = self.__fetch_weather_forecast_data()
        #print(data)
        return self.dialog_handler.format_forecast_output(self, time_range, data)

    def __get_city(self):
        """Gets the city from the user's input."""
        logging.info("📍Getting city...")
        city = self.parameters.get("geo-city")
        try:
            # If the city is not in the current context, try to get it from the output context
            if not city:
                city = self.result.get("outputContexts", [])[0].get("parameters", {}).get("geo-city", [])
            logging.info(f"📍city: {city[0]}")
            # Return the first city if multiple are provided
            return city[0]
        except Exception as e:
            logging.error(f"Failed to find 📍city: {e}")
            return None
    
    def __get_date(self):
        """Gets the date from the user's input."""
        logging.info("🕐 Getting date...")
        time = self.parameters.get("date-time")
        print(time)
        try:
            # If the city is not in the current context, try to get it from the output context
            if not time:
                time = self.result.get("outputContexts", [])[0].get("parameters", {}).get("date-time", [])
            logging.info(f"🕐 date: {time[0]}")
            # Return the first city if multiple are provided
            return time
        except Exception as e:
            logging.error(f"Failed to find 🕐 date: {e}")
            return None
       
        
    def process_request(self, request: Dict) -> Dict:
        """Processes incoming weather queries.

        This function is responsible for extracting information from the user’s request and 
        then invoking the necessary methods to retrieve the appropriate weather data.

        Args:
            request (dict): The user's query request.

        Returns:
            dict: A dictionary containing the response to the user.
        """
        
        logging.info("🔄 Request in progress…")
        try:
            # Extract query result from the request
            self.result = request.get("queryResult")
            self.query_text = self.result.get("queryText")
            logging.info(f"💬 User Intent: {self.query_text}")
            
            # Extract action and parameters from the result
            self.action = self.result.get("action")
            self.parameters = self.result.get("parameters")
            self.condition = self.parameters.get("weather-condition")
            self.temperature = self.parameters.get("temperature")
            self.wind_speed = self.parameters.get("wind-speed")
            
            # Get city from the user's input
            self.city = self.__get_city()
            if not self.city:
                logging.info("❌ No city detected. Trigger fallback -> Request City.")
                return self.dialog_handler.handle_missing_city()

            # Get date from the user's input
            self.time = self.__get_date()
            
            # Check if the date range is valid
            time = self.date_handler.check_date_range(self.time)
            if time is True:  # If the start date is in the past
                logging.info("❌ Start date is in the past. Trigger fallback.")
                return self.dialog_handler.handle_past_date()
            elif time is False:  # If the end date exceeds 5 days from today
                logging.info("❌ End date is more than 5 days from today. Trigger fallback.")
                return self.dialog_handler.handle_future_date()
            elif time is str:  # If there's an error response
                return time
            
        except Exception as e:
            logging.error(f"⛔ Error: {e}")
            return self.dialog_handler.handle_error()  # Handle general error
        
        try:
            # Fetch and format the weather data
            speech = self.__fetch_weather(time)
            logging.info(f"🔊 Response: {speech}")
            return {"fulfillmentText": speech, "displayText": speech}
        except Exception as e:
            logging.error(f"⛔ Error Fetching Weather Data: {e}")
            return self.dialog_handler.handle_error()  # Handle general error
