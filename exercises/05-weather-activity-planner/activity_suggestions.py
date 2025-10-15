"""
Activity Suggestions Based on Weather
Contains logic for recommending activities
"""


def calculate_comfort_index(temperature, humidity, wind_speed, units="metric"):
    """
    Calculate how comfortable it is outside (0-100 scale)
    Higher is more comfortable
    """
    # Adjust for temperature
    if units == "metric":
        ideal_temp = 22  # Celsius
        if temperature < 0:
            comfort = max(0, 50 + temperature * 2)
        elif temperature > 35:
            comfort = max(0, 100 - (temperature - 35) * 3)
        else:
            comfort = 100 - abs(temperature - ideal_temp) * 2
    else:  # imperial
        ideal_temp = 72  # Fahrenheit
        if temperature < 32:
            comfort = max(0, 50 + (temperature - 32) * 0.5)
        elif temperature > 95:
            comfort = max(0, 100 - (temperature - 95) * 2)
        else:
            comfort = 100 - abs(temperature - ideal_temp) * 1.5
    
    # Adjust for humidity
    if humidity > 80:
        comfort -= (humidity - 80) * 0.5
    elif humidity < 30:
        comfort -= (30 - humidity) * 0.3
    
    # Adjust for wind
    if wind_speed > 20:
        comfort -= (wind_speed - 20) * 1.5
    
    return max(0, min(100, comfort))


def suggest_activities(weather_condition, temperature, humidity, wind_speed, 
                      is_weekend=False, units="metric"):
    """
    Suggest activities based on weather conditions
    
    Returns:
        dict with activity suggestions
    """
    condition = weather_condition.lower()
    activities = {
        "outdoor": [],
        "indoor": [],
        "caution": []
    }
    
    # Calculate comfort
    comfort = calculate_comfort_index(temperature, humidity, wind_speed, units)
    
    # Determine temperature category
    if units == "metric":
        cold = temperature < 10
        cool = 10 <= temperature < 18
        mild = 18 <= temperature < 25
        warm = 25 <= temperature < 32
        hot = temperature >= 32
    else:  # imperial
        cold = temperature < 50
        cool = 50 <= temperature < 65
        mild = 65 <= temperature < 77
        warm = 77 <= temperature < 90
        hot = temperature >= 90
    
    # Sunny/Clear weather
    if condition in ["clear", "sunny"]:
        if hot:
            activities["outdoor"] = [
                "🏊 Swimming or water activities",
                "🌳 Morning or evening walk in the park",
                "🍦 Visit outdoor cafes (with shade)",
                "🚴 Early morning bike ride"
            ]
            activities["caution"] = ["☀️ Very hot! Stay hydrated and use sunscreen"]
        elif warm:
            activities["outdoor"] = [
                "🚴 Cycling or biking",
                "🏃 Jogging or running",
                "🧺 Picnic in the park",
                "🎾 Outdoor sports (tennis, volleyball)",
                "📸 Photography walk",
                "🎨 Visit outdoor markets or festivals"
            ]
        elif mild:
            activities["outdoor"] = [
                "🚶 City walking tour",
                "🌳 Hiking or nature trails",
                "☕ Outdoor dining",
                "🎪 Visit open-air attractions",
                "🏛️ Explore historical sites"
            ]
        elif cool:
            activities["outdoor"] = [
                "🚶 Brisk walk",
                "☕ Outdoor café (with a jacket)",
                "📸 Autumn photography"
            ]
            activities["caution"] = ["🧥 Bring a jacket or sweater"]
        else:  # cold
            activities["indoor"] = [
                "☕ Cozy cafes",
                "🏛️ Museums",
                "🎭 Theater or cinema",
                "🍽️ Indoor restaurants"
            ]
            activities["outdoor"] = ["⛸️ Ice skating", "⛷️ Winter sports"]
            activities["caution"] = ["🧣 Bundle up! It's cold outside"]
    
    # Cloudy weather
    elif condition in ["clouds", "cloudy", "overcast"]:
        activities["outdoor"] = [
            "🚶 Casual walk",
            "📸 Photography (great lighting!)",
            "🚴 Cycling",
            "🛍️ Outdoor shopping districts"
        ]
        activities["indoor"] = [
            "🏛️ Museums",
            "🎨 Art galleries",
            "📚 Libraries or bookstores",
            "☕ Cafes"
        ]
    
    # Rainy weather
    elif condition in ["rain", "drizzle", "shower"]:
        activities["indoor"] = [
            "🏛️ Museums and galleries",
            "🎬 Movie theater",
            "🛍️ Indoor shopping mall",
            "☕ Cozy café",
            "📚 Library or bookstore",
            "🎳 Bowling alley",
            "🎮 Gaming center",
            "🍽️ Try new restaurants"
        ]
        activities["outdoor"] = [
            "☔ Romantic walk with umbrella (light rain)",
            "🌧️ Puddle jumping (if you're adventurous!)"
        ]
        activities["caution"] = ["☔ Don't forget your umbrella!"]
    
    # Stormy weather
    elif condition in ["thunderstorm", "storm"]:
        activities["indoor"] = [
            "🏠 Stay indoors - perfect for Netflix!",
            "📚 Read a good book",
            "🎮 Video games",
            "🍳 Cook something special",
            "🎨 Indoor hobbies and crafts",
            "☕ Board games with friends"
        ]
        activities["caution"] = [
            "⚠️ Stay indoors! Thunderstorm warning",
            "⚡ Avoid outdoor activities"
        ]
    
    # Snowy weather
    elif condition in ["snow", "snowy"]:
        activities["outdoor"] = [
            "⛷️ Skiing or snowboarding",
            "⛸️ Ice skating",
            "⛄ Build a snowman",
            "📸 Winter photography"
        ]
        activities["indoor"] = [
            "☕ Hot chocolate at a café",
            "🏛️ Museums",
            "🎭 Theater",
            "🍲 Cozy restaurant"
        ]
        activities["caution"] = [
            "🧣 Dress warmly in layers",
            "⚠️ Watch for icy conditions"
        ]
    
    # Foggy/Misty weather
    elif condition in ["fog", "mist", "haze"]:
        activities["indoor"] = [
            "☕ Café with a view",
            "🏛️ Museums",
            "📚 Bookstores"
        ]
        activities["outdoor"] = [
            "📸 Atmospheric photography",
            "🚶 Mysterious walk (with caution)"
        ]
        activities["caution"] = ["🌫️ Limited visibility - drive carefully"]
    
    # Weekend bonus suggestions
    if is_weekend and comfort > 60:
        activities["outdoor"].insert(0, "🎪 Check local weekend events and festivals")
    
    return {
        "comfort_index": round(comfort, 1),
        "comfort_description": get_comfort_description(comfort),
        "outdoor_activities": activities["outdoor"],
        "indoor_activities": activities["indoor"],
        "cautions": activities["caution"]
    }


def get_comfort_description(comfort_index):
    """Get human-readable comfort description"""
    if comfort_index >= 80:
        return "Perfect weather! 😊"
    elif comfort_index >= 60:
        return "Comfortable 👍"
    elif comfort_index >= 40:
        return "Tolerable 😐"
    elif comfort_index >= 20:
        return "Uncomfortable 😕"
    else:
        return "Very uncomfortable ❌"


def should_bring_umbrella(forecast_data):
    """
    Analyze forecast to determine if umbrella is needed
    """
    rain_days = []
    
    for day in forecast_data.get("forecasts", []):
        condition = day.get("condition", "").lower()
        if "rain" in condition or "drizzle" in condition or "shower" in condition:
            rain_days.append(day["date"])
    
    if len(rain_days) >= 3:
        return {
            "recommendation": "Yes, definitely bring an umbrella! ☔",
            "reason": f"Rain expected on {len(rain_days)} days",
            "rainy_days": rain_days
        }
    elif len(rain_days) >= 1:
        return {
            "recommendation": "Yes, pack an umbrella to be safe ☂️",
            "reason": f"Rain possible on {len(rain_days)} day(s)",
            "rainy_days": rain_days
        }
    else:
        return {
            "recommendation": "No umbrella needed! ☀️",
            "reason": "No rain in the forecast",
            "rainy_days": []
        }


def get_best_day_for_activity(forecast_data, activity_type="outdoor"):
    """
    Find the best day in forecast for a specific activity type
    """
    if not forecast_data.get("success"):
        return None
    
    forecasts = forecast_data.get("forecasts", [])
    if not forecasts:
        return None
    
    # Score each day
    scored_days = []
    for day in forecasts:
        score = 0
        temp = day["temp_avg"]
        condition = day["condition"].lower()
        
        # Temperature scoring (metric)
        if 20 <= temp <= 26:
            score += 30
        elif 15 <= temp <= 30:
            score += 20
        elif 10 <= temp <= 35:
            score += 10
        
        # Condition scoring
        if activity_type == "outdoor":
            if "clear" in condition or "sun" in condition:
                score += 40
            elif "cloud" in condition:
                score += 20
            elif "rain" in condition or "storm" in condition:
                score -= 20
        
        # Humidity bonus
        if day["humidity"] < 70:
            score += 10
        
        scored_days.append({
            "date": day["date"],
            "score": score,
            "temp": day["temp_avg"],
            "condition": day["condition"]
        })
    
    # Sort by score
    scored_days.sort(key=lambda x: x["score"], reverse=True)
    best_day = scored_days[0]
    
    return {
        "best_date": best_day["date"],
        "temperature": round(best_day["temp"], 1),
        "condition": best_day["condition"],
        "all_days_ranked": scored_days
    }