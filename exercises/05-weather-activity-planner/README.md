# Exercise 05: Weather-Based Activity Planner

## 🎯 Overview
An intelligent AI assistant that helps you plan activities based on real-time weather data. The assistant uses multiple tools to fetch weather information, analyze conditions, and provide personalized activity recommendations.

## ✨ Features

### Real-Time Weather Data
- 🌡️ Current weather for any city worldwide
- 📅 5-day weather forecasts
- 🌬️ Wind speed, humidity, and pressure data
- 🌤️ Weather condition descriptions

### Smart Analysis
- 📊 Comfort index calculation (0-100 scale)
- ☔ Umbrella recommendation system
- 📆 Best day finder for outdoor activities
- 🎯 Weather-based activity suggestions

### Activity Recommendations
- 🏃 Outdoor activities (hiking, cycling, picnics, sports)
- 🏛️ Indoor activities (museums, cafes, shopping, entertainment)
- ⚠️ Weather cautions and safety tips
- 🧥 Clothing and preparation suggestions

## 🎓 Learning Objectives

This exercise demonstrates:

### 1. **Real API Integration**
- Working with OpenWeatherMap API
- Handling API authentication
- Error handling and rate limiting
- Data parsing and transformation

### 2. **LLM Tool Use (Function Calling)**
- Defining tool schemas with JSON Schema
- Implementing actual functions
- Mapping tools to implementations
- Handling tool call requests and responses
- Chaining multiple tools together

### 3. **Complex Data Processing**
- Grouping time-series data by day
- Calculating aggregates (min, max, avg)
- Finding most common values
- Data transformation and formatting

### 4. **Conversational AI Design**
- Natural language understanding
- Context-aware responses
- Multi-turn conversations
- Tool orchestration based on user intent

### 5. **User Experience**
- Clear, helpful responses
- Emoji usage for engagement
- Practical recommendations
- Error handling with friendly messages

## 🚀 Setup

### Prerequisites
- Python 3.8+
- OpenAI API key
- OpenWeatherMap API key (free tier)


## 🔧 Tools Implemented

### 1. **get_current_weather**
Fetches real-time weather for a city
```python
Input: city, units (metric/imperial)
Output: temperature, humidity, wind, condition, etc.
```

### 2. **get_weather_forecast**
Gets 5-day weather forecast
```python
Input: city, days (1-5), units
Output: daily summaries with temp ranges and conditions
```

### 3. **calculate_comfort_index**
Calculates how comfortable it is outside (0-100)
```python
Input: temperature, humidity, wind_speed
Output: comfort score and description
```

### 4. **suggest_activities**
Recommends activities based on weather
```python
Input: weather_condition, temperature, humidity, wind
Output: outdoor activities, indoor activities, cautions
```

### 5. **should_bring_umbrella**
Analyzes forecast for rain
```python
Input: forecast_data
Output: recommendation and rainy days
```

### 6. **get_best_day_for_activity**
Finds optimal day in forecast
```python
Input: forecast_data, activity_type
Output: best date with reasoning
```
