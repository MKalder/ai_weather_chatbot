from collections import defaultdict, Counter
from datetime import datetime
from typing import Final
import json
import random
import logging

from weather_condition.precipitation import condition_emojis

FMT: Final = "%Y-%m-%d"

class DialogHandler:
    def __init__(self):
        pass
    @staticmethod
    def _generate_response(responses: list) -> dict:
        resp = random.choice(responses)
        return {"fulfillmentText": resp, "displayText": resp}

    def handle_past_date(self) -> dict:
        responses = [
            "I'm sorry, I can't provide weather data for the past.",
            "I can only give forecasts for today and the next 5 days. ☀️🌧️",
            "I can only provide weather data for today and up to 5 days ahead. ⏳",
            "I only have forecasts for today and the next 5 days. Ask away! 😊",
            "Need a forecast? I cover today and the next 5 days! 🌍"
        ]
        return self._generate_response(responses)

    def handle_future_date(self) -> dict:
        responses = [
            "I’m sorry, but I can only provide weather forecasts for the next 5 days.",
            "Unfortunately, I can’t predict the weather beyond 5 days.",
            "I can only provide forecasts for up to 5 days ahead.",
            "I’m sorry, but my forecast limit is 5 days ahead."
        ]
        return self._generate_response(responses)

    def handle_missing_city(self) -> dict:
        responses = [
            "Which city do you want the weather for? 🌍",
            "Tell me a city, and I'll fetch the forecast! ☀️🌧",
            "Where should I check the weather for? 🏙️",
            "Just type a city, and I'll get the forecast! 🌍"
        ]
        return self._generate_response(responses)

    def handle_error(self) -> dict:
        responses = [
            "I'm sorry, I couldn't fetch the weather. Can you please try again?",
            "Oops! Something went wrong while fetching the weather.",
            "I'm having trouble fetching the weather. Can you please try again?"
        ]
        return self._generate_response(responses)
    
    def __select_dates(self, time, selected_dates):
        """
        Selects the dates from the selected_dates list that are within the given time range.

        If the time range is a single day, only that day is selected. If the time range is a range of days, all days within that range are selected.

        Args:
            time (tuple): A tuple of two datetime objects representing the start and end of the time range.
            selected_dates (list): A list of strings representing the dates to be selected.

        Returns:
            list: A list of strings representing the selected dates.
        """
        if time[0] == time[1]:
            # If the time range is a single day, only select that day
            print(f"time[0] == time[1]: {time[0]}")
            for date in selected_dates:
                if date == time[0].strftime(FMT):
                    selected_dates = [date]
        else:
            # If the time range is a range of days, select all days within that range
            print(f"time[0] != time[1]: {time[0]}")
            start_dt = time[0].strftime(FMT)
            end_dt = time[1].strftime(FMT)
            selected_dates = [date for date in selected_dates if start_dt <= date <= end_dt]
        
        return selected_dates
    
    def __find_weather_attribute(self, attribute_name, attribute_list):
        """
        Finds and returns the emoji for a given weather attribute from the attribute list.

        Args:
            attribute_name (str): The name of the weather attribute to find.
            attribute_list (list): A list of attributes from which to find the emoji.

        Returns:
            str or None: The emoji representing the attribute or None if not found.
        """
        logging.info(f"🔎 Finding {attribute_name}..")
        
        # Check if the attribute list is not empty
        if attribute_list:
            print(f"{attribute_name.capitalize()}: {attribute_list}")
            print(f"Type: {type(attribute_list[0])}")
            print(f"Attribute List: {attribute_list}")
            
            # Get the emoji for the first attribute in the list, if it exists
            return condition_emojis.get(attribute_list[0].lower(), None)
        else:
            # Return None if the attribute list is empty
            return None

    def __emoij_condition(self, condition: list) -> str:
        """
        Finds and returns the emoji for the first condition in the list.

        Args:
            condition (list): A list of weather conditions.

        Returns:
            str: The emoji representing the condition.
        """
        # Find the emoji for the first condition in the list
        return self.__find_weather_attribute("condition", condition)
       
    def __forecast_body(self, selected_dates, daily_forecasts) -> list:
        """Formats the forecast body using the data from the API response.

        Args:
            selected_dates (list): A list of selected dates for which to format the forecast.
            daily_forecasts (dict): A dictionary of daily forecasts with the date as the key.

        Returns:
            list: A list of formatted forecast entries.
        """
        forecast = []
        
        # Iterate over the selected dates
        for date in selected_dates:
            daily_entries = daily_forecasts.get(date, [])
            if not daily_entries:
                continue  # Skip if no forecast data available
            
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%A, %b %d, %Y")

            # Determine the most common weather description
            weather_descriptions = [entry['weather'][0]['description'].title() for entry in daily_entries]
            most_common_weather = Counter(weather_descriptions).most_common(1)
            most_common_weather = most_common_weather[0][0] if most_common_weather else "Unknown"

            # Determine the temperature range
            temperatures = [entry['main']['temp'] for entry in daily_entries]
            min_temp, max_temp = (min(temperatures), max(temperatures)) if temperatures else (0, 0)
            temp_info = f"🔽 {min_temp:.1f}°C → 🔼 {max_temp:.1f}°C"

            # Determine the most common wind speed
            wind_speeds = [entry['wind']['speed'] for entry in daily_entries]
            most_common_wind_speed = Counter(wind_speeds).most_common(1)
            most_common_wind_speed = most_common_wind_speed[0][0] if most_common_wind_speed else 0

            # Assemble the forecast
            forecast.append({
                "date": formatted_date,
                "weather": most_common_weather,
                "temperature": temp_info,
                "wind_speed": f"{most_common_wind_speed} m/s"
            })
        
        logging.info("📅⚙️ Formatting forecast body complete")  # Log after processing
        return forecast
    
    def __forecast_body_condition(self, selected_dates, daily_forecasts, condition) -> str:
        """
        Formats the forecast body with the weather condition.

        Args:
            selected_dates (list): A list of selected dates for which to format the forecast.
            daily_forecasts (dict): A dictionary of daily forecasts with the date as the key.
            condition (list): A list of weather conditions to find in the forecast.

        Returns:
            str: The formatted forecast body with the weather condition.
        """
        logging.info(f"📅⚙️ Formatting forecast body {condition}")
        forecast = []
        
        common_weather = []
        print(f"Type: {type(condition)}")
        for date in selected_dates: 
            daily_entries = daily_forecasts[date] 
            for entry in daily_entries:
                print(entry['weather'][0]['description'].lower())
                for i in condition:
                    if i in entry['weather'][0]['description'].lower():
                        common_weather.append(entry['weather'][0]['description'].title())
                    else:
                        common_weather.append(f"No {i}")
            
            print(f"Common Weather: {common_weather}")
            common_we = Counter(common_weather).most_common(1)[0][0]
             
            emoji = self.__emoij_condition(condition)
            common_w = f"{emoji} {common_we}"   
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%A, %b %d, %Y")
             
             # Assemble the forecast
            forecast.append({
                "date": formatted_date,
                "weather": common_w
            })      
                                
        return forecast
    
    def __forecast_body_temperature(self, selected_dates, daily_forecasts, temperature) -> str:
        """
        Formats the forecast body by extracting the minimum and maximum temperatures from the daily forecasts.
        
        Args:
            selected_dates (list): A list of selected dates for which to format the forecast.
            daily_forecasts (dict): A dictionary of daily forecasts with the date as the key.
            temperature (list): A list of temperature options to find in the forecast.
            
        Returns:
            str: The formatted forecast body with the temperature information.
        """
        print(f"📅⚙️ Formatting forecast body {temperature}")
        forecast = []
        
        # Iterate over the selected dates
        for date in selected_dates:
            print("For loop ONE")
            daily_entries = daily_forecasts[date] 
             
            # Extract the temperatures from the daily entries
            temperatures = [entry['main']['temp'] for entry in daily_entries]
            min_temp, max_temp = min(temperatures), max(temperatures)
            temp_info = f"🔽 {min_temp:.1f}°C \n 🔼{max_temp:.1f}°C"
                 
            # Format the date
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%A, %b %d, %Y")
                
            # Assemble the forecast
            forecast.append({
                "date": formatted_date,
                "temperature": temp_info
            })
        
        logging.info("📅⚙️ Formatting forecast body complete")             
        return forecast
    
    def __forecast_body_wind_speed(self, selected_dates, daily_forecasts, wind_speed) -> str:
        """
        Formats the forecast body by extracting the minimum and maximum wind speeds from the daily forecasts.
        
        Args:
            selected_dates (list): A list of selected dates for which to format the forecast.
            daily_forecasts (dict): A dictionary of daily forecasts with the date as the key.
            wind_speed (list): A list of wind speed options to find in the forecast.
            
        Returns:
            str: The formatted forecast body with the wind speed information.
        """
        print(f"📅⚙️ Formatting forecast body {wind_speed}")
        forecast = []
        
        # Iterate over the selected dates
        for date in selected_dates:
            print("For loop ONE")
            daily_entries = daily_forecasts[date] 
             
            # Extract the wind speeds from the daily entries
            wind_speeds = [entry['wind']['speed'] for entry in daily_entries]
            min_wind, max_wind = min(wind_speeds), max(wind_speeds)
            common_wind_speed  = f"🔽 {min_wind:.1f} m/s → 🔼 {max_wind:.1f} m/s"
                
            # Format the date
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%A, %b %d, %Y")
                
            # Assemble the forecast
            forecast.append({
                "date": formatted_date,
                "wind_speed": f"{common_wind_speed} m/s"
            })
                                   
        return forecast
    
    def __forecast_formatter(self, selected_dates: list, forecast_data: dict, daily_forecasts: dict, condition=None, temperature=None, wind_speed=None) -> dict:
        """
        Formats the forecast output according to the specified condition, temperature, or wind speed.
        
        Args:
            selected_dates (list): A list of selected dates for which to format the forecast.
            forecast_data (dict): A dictionary of forecast data returned from the OpenWeatherMap API.
            daily_forecasts (dict): A dictionary of daily forecasts with the date as the key.
            condition (str, optional): The condition to filter the forecast by. Defaults to None.
            temperature (str, optional): The temperature to filter the forecast by. Defaults to None.
            wind_speed (str, optional): The wind speed to filter the forecast by. Defaults to None.
            
        Returns:
            dict: The forecast output as a dictionary.
        """
        print("📅⚙️ Formatting forecast output...")
        forecast_report = {
             "location": forecast_data["city"]["name"]
        }
        
        if condition:
            # Filter the forecast by condition
            #forecast_report += self.__forecast_body_condition(selected_dates, daily_forecasts, condition)
            forecast_report["conditions"]=(self.__forecast_body_condition(selected_dates, daily_forecasts, condition))
            #return forecast_report 
        elif temperature:
            # Filter the forecast by temperature
            #forecast_report += self.__forecast_body_temperature(selected_dates, daily_forecasts, temperature)
            forecast_report["conditions"]=(self.__forecast_body_temperature(selected_dates, daily_forecasts, temperature))
            #return  forecast_report
        elif wind_speed:
            # Filter the forecast by wind speed
            #forecast_report += self.__forecast_body_wind_speed(selected_dates, daily_forecasts, wind_speed)
            forecast_report["conditions"]=(self.__forecast_body_wind_speed(selected_dates, daily_forecasts, wind_speed))
            #return forecast_report
        else:
            # Return the full forecast
            #forecast_report += self.__forecast_body(selected_dates, daily_forecasts)
            forecast_report["conditions"]=(self.__forecast_body(selected_dates, daily_forecasts))
        
        return forecast_report

    def format_weather_response(self, forecast: dict) -> json:
        logging.info("📅⚙️ Formatting weather response...")

        location = forecast.get("location", "Unknown Location")  
        conditions = forecast.get("conditions", "Unknown Conditions")  
        # Create forecast messages for multiple days
        forecast_texts = []
        
        for day in conditions:
            print(day)
            details = []

            # Add only if not "Unknown"
            if day.get('date') and day.get('date') != "Unknown Date":
                details.append(f"📅 {day['date']}")
            if day.get('weather') and day.get('weather') != "Unknown":
                details.append(f"⛅ Weather: {day['weather']}")
            if day.get('temperature') and day.get('temperature') != "Unknown":
                details.append(f"🌡️ Temperature: {day['temperature']}")
            if day.get('wind_speed') and day.get('wind_speed') != "Unknown":
                details.append(f"💨 Wind Speed: {day['wind_speed']}")

            if details:  # Only add if there’s at least one valid detail
                forecast_texts.append("\n".join(details))

            # Build response
            response = {
                "fulfillmentMessages": [
                    {
                        "platform": "PLATFORM_UNSPECIFIED",
                        "payload": {
                            "richContent": [
                                [
                                    {
                                        "type": "description",
                                        "title": "Weather Forecast",
                                        "text": [
                                            f"📍 {location}",
                                            *forecast_texts,  
                                        ]
                                    }
                                ]
                            ]
                        }
                    }
                ]
            }

        return response
    
    def format_forecast_output(self, weather, time, forecast_data: dict) -> str:
        """
        Formats the forecast output based on the specified condition, temperature, or wind speed.
        
        Args:
            weather (Weather): The Weather object containing the condition, temperature, and wind speed options.
            time (str): The time range for which to format the forecast.
            forecast_data (dict): A dictionary of forecast data returned from the OpenWeatherMap API.
            
        Returns:
            str: The formatted forecast output.
        """
        
        # Group forecast entries by date
        logging.info("📅⚙️ Grouping forecast entries by date...")
        daily_forecasts = defaultdict(list)
        for forecast in forecast_data['list']:
            date_str = forecast['dt_txt'].split()[0]
            daily_forecasts[date_str].append(forecast)

        sorted_dates = sorted(daily_forecasts.keys())
        selected_dates = sorted_dates[:6]
        
        # Select the dates based on the time range
        selected_dates = self.__select_dates(time, selected_dates)
        print(selected_dates)
            
        # Format the forecast
        forecast = self.__forecast_formatter(selected_dates, forecast_data, daily_forecasts, weather.condition, weather.temperature, weather.wind_speed)
        formatted = self.format_weather_response(forecast)

        return formatted
