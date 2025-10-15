"""
Weather API Integration
Handles all calls to OpenWeatherMap API
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5"


def get_current_weather(city, units="metric"):
    """
    Get current weather for a city
    
    Args:
        city (str): City name (e.g., "Paris", "New York")
        units (str): "metric" (Celsius) or "imperial" (Fahrenheit)
    
    Returns:
        dict: Weather data or error
    """
    try:
        url = f"{BASE_URL}/weather"
        params = {
            "q": city,
            "appid": API_KEY,
            "units": units
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        return {
            "success": True,
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "main_condition": data["weather"][0]["main"],
            "icon": data["weather"][0]["icon"],
            "units": units
        }
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"success": False, "error": f"City '{city}' not found"}
        return {"success": False, "error": f"API error: {str(e)}"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}


def get_weather_forecast(city, days=5, units="metric"):
    """
    Get weather forecast for next 5 days
    
    Args:
        city (str): City name
        days (int): Number of days (1-5)
        units (str): "metric" or "imperial"
    
    Returns:
        dict: Forecast data or error
    """
    try:
        url = f"{BASE_URL}/forecast"
        params = {
            "q": city,
            "appid": API_KEY,
            "units": units,
            "cnt": days * 8  # API returns 3-hour intervals, 8 per day
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Process forecast data - group by day
        daily_forecasts = []
        current_date = None
        daily_temps = []
        daily_conditions = []
        
        for item in data["list"]:
            date = item["dt_txt"].split()[0]  # Extract date
            
            if date != current_date:
                if daily_temps:  # Save previous day
                    daily_forecasts.append({
                        "date": current_date,
                        "temp_min": min(daily_temps),
                        "temp_max": max(daily_temps),
                        "temp_avg": sum(daily_temps) / len(daily_temps),
                        "condition": max(set(daily_conditions), key=daily_conditions.count),
                        "humidity": item["main"]["humidity"]
                    })
                
                current_date = date
                daily_temps = []
                daily_conditions = []
            
            daily_temps.append(item["main"]["temp"])
            daily_conditions.append(item["weather"][0]["main"])
        
        # Add last day
        if daily_temps:
            daily_forecasts.append({
                "date": current_date,
                "temp_min": min(daily_temps),
                "temp_max": max(daily_temps),
                "temp_avg": sum(daily_temps) / len(daily_temps),
                "condition": max(set(daily_conditions), key=daily_conditions.count),
                "humidity": data["list"][-1]["main"]["humidity"]
            })
        
        return {
            "success": True,
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "forecasts": daily_forecasts[:days],
            "units": units
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


