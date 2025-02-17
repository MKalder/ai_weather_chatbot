from datetime import datetime, timedelta
from dateutil import parser 
from typing import Dict
import logging

from .dialog import DialogHandler

class DateHandler():
    def __init__(self):
        self.time = None
        self.dialog_handler = DialogHandler()
    
    def check_date_range(self, time: Dict):
        """Validates and extracts start and end dates from `self.time`.

        Checks if the parsed start and end dates are within the allowable range 
        (from current date to 5 days ahead). Handles errors if date strings are 
        missing or parsing fails.

        Returns:
            tuple or bool: Returns a tuple of start and end dates if valid, 
                           True if the start date is in the past, 
                           False if the end date exceeds the maximum allowable date.
        """
        print(f"self.time: {time}")
        self.time = time 
        current_date = datetime.now().astimezone().date()  # Get the current date
        max_end_date = current_date + timedelta(days=5)    # Calculate maximum allowed end date

        print("Checking date range...") # Debugging output
        logging.info("📏Checking date range...")

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
        logging.info(f"Date validation outcome: {outcome}")  # Debugging output
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
            logging.info("Get the start and end dates from the dictionary")
            start_str = self.time.get("startDate") or self.time.get("startDateTime") or self.time.get("date_time")
            end_str = self.time.get("endDate") or self.time.get("endDateTime") or self.time.get("date_time")

        # Check if the time parameter is a list
        elif isinstance(self.time, list):
            # Check if the list contains a dictionary
            if len(self.time) == 1 and isinstance(self.time[0], dict):
                time_dict = self.time[0]
                start_str = time_dict.get("startDate") or time_dict.get("startDateTime") or time_dict.get("date_time")
                end_str = time_dict.get("endDate") or time_dict.get("endDateTime") or time_dict.get("date_time")
            # Check if the list contains a string
            elif len(self.time) == 1 and isinstance(self.time[0], str):
                start_str = end_str = self.time[0]
            # If the list contains more than one element, use the first two
            elif len(self.time) > 1:
                start_str = self.time[0]
                end_str = self.time[1]
            # If the list is empty, use the current date
            else:
                start_str = end_str = current_date.strftime("%Y-%m-%d")
        # Check if the time parameter is a string        
        elif isinstance(self.time, str):
            start_str = end_str = self.time
        # If the time parameter is not a dictionary or list, use the current date
        else:
            start_str = end_str = current_date.strftime("%Y-%m-%d")

        logging.info(f"start_str: {start_str} | end_str: {end_str}")

        # Check if the end date is a dictionary
        if isinstance(end_str, dict):
            # Get the end date from the dictionary
            end_str = end_str.get("endDate") or end_str.get("startDate")

        # Handle errors if the date strings are missing or parsing fails
        if not start_str or not end_str:
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
