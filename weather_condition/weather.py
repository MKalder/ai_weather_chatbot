import requests
from datetime import datetime, timedelta
from dateutil import parser
import logging
import dialog_class as dialog
from dotenv import load_dotenv
import os 

# Load the .env file
load_dotenv()

# Access the keys
owm_key = os.getenv("OWM_KEY")

# Configure the logger
# logging.basicConfig(
#     filename='weather_query.log',  # Name of the log file
#     level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
#     datefmt='%Y-%m-%d %H:%M:%S'  # Date format
# )

class Weather:
    """Weather class for interacting with weather data from OpenWeatherMap API."""
    
    def __init__(self):
        """Initialize the Weather class with necessary attributes."""
        self.owm_api_key = owm_key  # OpenWeatherMap API key
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"  # Base URL for weather data forecast 5 days
        self.city = None  # City for which to fetch the weather
        self.time = None  # Time range for weather data
        self.condition = None  # Weather condition
        self.temperature = None  # Temperature data
        self.wind_speed = None  # Wind speed data
        self.dialog_handler = dialog.DialogHandler()  # Handler for dialog responses
        
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

    def __check_date_range(self):
        """Validates and extracts start and end dates from `self.time`.

        Checks if the parsed start and end dates are within the allowable range 
        (from current date to 5 days ahead). Handles errors if date strings are 
        missing or parsing fails.

        Returns:
            tuple or bool: Returns a tuple of start and end dates if valid, 
                           True if the start date is in the past, 
                           False if the end date exceeds the maximum allowable date.
        """
        current_date = datetime.now().astimezone().date()  # Get the current date
        max_end_date = current_date + timedelta(days=5)    # Calculate maximum allowed end date

        print("Checking date range...")  # Debugging output

        # Extract date strings from time parameters
        start_str, end_str = self.__extract_date_strings(current_date)
        if not start_str or not end_str:
            return self.dialog_handler.handle_error()  # Handle error if date strings are missing

        # Parse the date strings into date objects
        start_dt, end_dt = self.__parse_dates(start_str, end_str)
        if start_dt is None or end_dt is None:
            return self.dialog_handler.handle_error()  # Handle error if parsing fails

        # Validate the parsed dates against the allowed range
        outcome = self.__validate_date_range(start_dt, end_dt, current_date, max_end_date)
        print(f"outcome: {outcome}")  # Debugging output
        print(f"typeof outcome: {type(outcome)}")  # Debugging output
        return outcome  # Return the validation outcome
        
    def __extract_date_strings(self, current_date):
        """Extracts date strings from `self.time` in different formats.

        The `self.time` parameter can be a dictionary with start and end dates,
        a list of two dates, or a single date string. Handles errors if the
        date strings are missing or parsing fails.
        """
        start_str = end_str = None

        # Check if the time parameter is a dictionary
        if isinstance(self.time, dict):
            # Get the start and end dates from the dictionary
            print("Get the start and end dates from the dictionary")
            start_str = self.time.get("startDate") or self.time.get("startDateTime") or self.time.get("date_time")
            end_str = self.time.get("endDate") or self.time.get("endDateTime") or self.time.get("date_time")

        # Check if the time parameter is a list
        elif isinstance(self.time, list):
            # Check if the list contains a dictionary
            if len(self.time) == 1 and isinstance(self.time[0], dict):
                print("Check if the list contains a dictionary")
                time_dict = self.time[0]
                start_str = time_dict.get("startDate") or time_dict.get("startDateTime") or time_dict.get("date_time")
                end_str = time_dict.get("endDate") or time_dict.get("endDateTime") or time_dict.get("date_time")
            # Check if the list contains a string
            elif len(self.time) == 1 and isinstance(self.time[0], str):
                print("Check if the list contains a string")
                start_str = end_str = self.time[0]
            # If the list contains more than one element, use the first two
            elif len(self.time) > 1:
                print("If the list contains more than one element, use the first two")
                start_str = self.time[0]
                end_str = self.time[1]
            # If the list is empty, use the current date
            else:
                print("If the list is empty, use the current date")
                start_str = end_str = current_date.strftime("%Y-%m-%d")
                
        elif isinstance(self.time, str):
            print("If the time parameter is a string, use it as the start and end dates")
            start_str = end_str = self.time
        # If the time parameter is not a dictionary or list, use the current date
        else:
            print("If the time parameter is not a dictionary or list, use the current date")
            start_str = end_str = current_date.strftime("%Y-%m-%d")

        # Print the extracted date strings
        print(f"start_str: {start_str} | end_str: {end_str}")

        # Check if the end date is a dictionary
        if isinstance(end_str, dict):
            # Get the end date from the dictionary
            end_str = end_str.get("endDate") or end_str.get("startDate")

        # Handle errors if the date strings are missing or parsing fails
        if not start_str or not end_str:
            print("⛔ No valid start or end date found!")
            logging.error("⛔ No valid start or end date found!")
            return self.dialog_handler.handle_error()

        return start_str, end_str
    
    def __parse_dates(self, start_str, end_str):
        """Parses date strings into `datetime.date` objects.

        Args:
            start_str (str): Start date string to parse.
            end_str (str): End date string to parse.

        Returns:
            tuple: A tuple of two `datetime.date` objects,
                   or `(None, None)` if parsing fails.
        """
        try:
            # Parse the date strings into datetime objects
            start_dt = parser.parse(start_str)
            end_dt = parser.parse(end_str)
            # Return the parsed date objects
            return start_dt.date(), end_dt.date()
        except (TypeError, ValueError) as e:
            # Log an error if parsing fails
            logging.error(f"⛔ Error parsing date! {e}")
            # Return None on failure
            return None, None

    def __validate_date_range(self, start_dt, end_dt, current_date, max_end_date):
        """Validates whether the given start and end dates are within the permissible range.

        Args:
            start_dt (datetime.date): The parsed start date.
            end_dt (datetime.date): The parsed end date.
            current_date (datetime.date): The current date.
            max_end_date (datetime.date): The maximum allowed end date.

        Returns:
            tuple: A tuple containing start_dt and end_dt if within range.
            bool: True if the start date is in the past.
            bool: False if the end date exceeds the maximum allowable date.
        """
        # Check if the start date is in the past
        if start_dt < current_date:
            return True  # Return True to indicate a past date error
        
        # Check if the end date exceeds the maximum permissible date
        elif end_dt > max_end_date:
            return False  # Return False to indicate a future date error
        
        # Return the start and end dates if both are within the permissible range
        return start_dt, end_dt

    def __get_city(self):
        """Gets the city from the user's input."""
        print("📍Getting city...")
        logging.info("📍Getting city...")
        city = self.parameters.get("geo-city")
        try:
            # If the city is not in the current context, try to get it from the output context
            if not city:
                city = self.result.get("outputContexts", [])[0].get("parameters", {}).get("geo-city", [])
            # Return the first city if multiple are provided
            return city[0]
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def __get_date(self):
        """Gets the date from the user's input."""
        print("🕐 Getting date...")
        logging.info("🕐 Getting date...")
        time = self.parameters.get("date-time")
        print(time)
        try:
            # If the city is not in the current context, try to get it from the output context
            if not time:
                time = self.result.get("outputContexts", [])[0].get("parameters", {}).get("date-time", [])
            # Return the first city if multiple are provided
            return time[0]
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def process_request(self, request):
        """Processes incoming weather queries.

        This function is responsible for getting the information from the
        user's request and calling the necessary methods to process the
        request.

        Args:
            request (dict): The user's query request.

        Returns:
            dict: A dictionary containing the response to the user.
        """
        print("\n🔄 Request in progress…")
        logging.info("🔄 Request in progress…")
        try:
            self.result = request.get("queryResult")
            self.query_text = self.result.get("queryText")
            logging.info(f"💬 User Intent: {self.query_text}")
            self.action = self.result.get("action")
            self.parameters = self.result.get("parameters")
            self.condition = self.parameters.get("weather-condition")
            self.temperature = self.parameters.get("temperature")
            self.wind_speed = self.parameters.get("wind-speed")
            
            self.city = self.__get_city()
            print(f"City: {self.city}")
            print(f"Type City: {type(self.city)}")
            if not self.city:
                logging.info("❌ No city detected. Trigger fallback.")
                return self.dialog_handler.handle_missing_city()

            #self.time = self.parameters.get("date-time")
            self.time = self.__get_date()
            print(f"time: {self.time}")
            print(f"type: {type(self.time)}")
            time = self.__check_date_range()
            print(f"time: {time}")
            if time is True:  # If it's a string, it's an error response
                logging.info("❌ Start date is in the past. Trigger fallback.")
                return self.dialog_handler.handle_past_date()  # Handle past date
            elif time is False:
                logging.info("❌ End date is more than 5 days from today. Trigger fallback.")
                return self.dialog_handler.handle_future_date()  # Handle future date
            elif time is str:
                return time
            
        except Exception as e:
            logging.error(f"⛔ Error: {e}")
            return self.dialog_handler.handle_error()  # Handle general error
        try:
            speech = self.__fetch_weather(time)
            logging.info(f"🔊 Response: {speech}")
            return {"fulfillmentText": speech, "displayText": speech}
        except Exception as e:
            logging.error(f"⛔ Error Fetching Weather Data: {e}")
            return self.dialog_handler.handle_error()  # Handle general error
