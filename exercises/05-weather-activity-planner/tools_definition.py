"""
Tool Definitions for LLM
Defines all available tools and their schemas
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get current weather conditions for a specific city. Use this when user asks about current weather, temperature, or conditions right now.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name, e.g., 'Paris', 'New York', 'Tokyo'"
                    },
                    "units": {
                        "type": "string",
                        "enum": ["metric", "imperial"],
                        "description": "Temperature units: 'metric' for Celsius, 'imperial' for Fahrenheit. Default to metric unless user specifies."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_forecast",
            "description": "Get weather forecast for the next 1-5 days. Use this when user asks about future weather, upcoming days, or planning ahead.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to forecast (1-5). Default to 5 if not specified.",
                        "minimum": 1,
                        "maximum": 5
                    },
                    "units": {
                        "type": "string",
                        "enum": ["metric", "imperial"],
                        "description": "Temperature units"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_comfort_index",
            "description": "Calculate how comfortable it is outside based on temperature, humidity, and wind. Returns a score from 0-100 where higher is more comfortable.",
            "parameters": {
                "type": "object",
                "properties": {
                    "temperature": {
                        "type": "number",
                        "description": "Temperature value"
                    },
                    "humidity": {
                        "type": "number",
                        "description": "Humidity percentage (0-100)"
                    },
                    "wind_speed": {
                        "type": "number",
                        "description": "Wind speed"
                    },
                    "units": {
                        "type": "string",
                        "enum": ["metric", "imperial"],
                        "description": "Units being used"
                    }
                },
                "required": ["temperature", "humidity", "wind_speed"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "suggest_activities",
            "description": "Suggest indoor and outdoor activities based on current weather conditions. Use this when user asks what to do, activities recommendations, or how to spend their time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "weather_condition": {
                        "type": "string",
                        "description": "Main weather condition (e.g., 'Clear', 'Clouds', 'Rain', 'Snow', 'Thunderstorm')"
                    },
                    "temperature": {
                        "type": "number",
                        "description": "Current temperature"
                    },
                    "humidity": {
                        "type": "number",
                        "description": "Humidity percentage"
                    },
                    "wind_speed": {
                        "type": "number",
                        "description": "Wind speed"
                    },
                    "is_weekend": {
                        "type": "boolean",
                        "description": "Whether it's currently weekend (Saturday or Sunday)"
                    },
                    "units": {
                        "type": "string",
                        "enum": ["metric", "imperial"],
                        "description": "Temperature units"
                    }
                },
                "required": ["weather_condition", "temperature", "humidity", "wind_speed"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "should_bring_umbrella",
            "description": "Analyze weather forecast to determine if an umbrella is needed. Use this when user asks about bringing an umbrella or rain protection.",
            "parameters": {
                "type": "object",
                "properties": {
                    "forecast_data": {
                        "type": "object",
                        "description": "Forecast data from get_weather_forecast function"
                    }
                },
                "required": ["forecast_data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_best_day_for_activity",
            "description": "Find the best day in the forecast for outdoor activities. Use this when user asks about the best time to visit, when to plan outdoor activities, or which day is best.",
            "parameters": {
                "type": "object",
                "properties": {
                    "forecast_data": {
                        "type": "object",
                        "description": "Forecast data from get_weather_forecast function"
                    },
                    "activity_type": {
                        "type": "string",
                        "enum": ["outdoor", "indoor"],
                        "description": "Type of activity being planned"
                    }
                },
                "required": ["forecast_data"]
            }
        }
    }
]