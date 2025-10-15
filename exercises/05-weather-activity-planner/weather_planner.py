"""
Exercise 05: Weather-Based Activity Planner
Main application with Gradio interface and LLM tool integration
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Import our modules
from weather_api import get_current_weather, get_weather_forecast
from activity_suggestions import (
    calculate_comfort_index,
    suggest_activities,
    should_bring_umbrella,
    get_best_day_for_activity
)
from tools_definition import tools

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"

# Map function names to actual functions
available_functions = {
    "get_current_weather": get_current_weather,
    "get_weather_forecast": get_weather_forecast,
    "calculate_comfort_index": calculate_comfort_index,
    "suggest_activities": suggest_activities,
    "should_bring_umbrella": should_bring_umbrella,
    "get_best_day_for_activity": get_best_day_for_activity
}

# System message for the LLM
SYSTEM_MESSAGE = """You are a friendly and helpful weather assistant and activity planner. Your goal is to help users plan their activities based on weather conditions.

Your capabilities:
1. Get current weather for any city
2. Get weather forecasts for the next 5 days
3. Calculate comfort index based on weather conditions
4. Suggest activities (indoor and outdoor) based on weather
5. Determine if an umbrella is needed
6. Find the best day for outdoor activities

Guidelines:
- Always be enthusiastic and helpful
- Use weather emojis to make responses engaging (☀️🌧️❄️⛅🌤️)
- When suggesting activities, provide variety (outdoor and indoor options)
- If weather is bad, emphasize indoor activities but stay positive
- Include practical tips (bring umbrella, wear sunscreen, dress warmly, etc.)
- When showing forecasts, format them clearly by day
- Always specify the city and country in your responses
- Use Celsius by default unless user specifies Fahrenheit

Example responses:
- "Perfect day in Paris! ☀️ It's 22°C and sunny - great for a picnic in Luxembourg Gardens!"
- "Looks like rain tomorrow in London 🌧️ - perfect weather for visiting the British Museum!"
- "It'll be quite windy (25 km/h) - maybe skip the outdoor café and try that cozy bookshop instead?"

Be conversational, informative, and always weather-aware!"""


def chat_with_tools(message, history):
    """
    Main chat function that handles tool calling
    """
    # Convert Gradio history format to OpenAI format
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
    
    
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}] + history + [{"role": "user", "content": message}]
    
    # Check if it's weekend (for activity suggestions)
    is_weekend = datetime.now().weekday() >= 5  # 5=Saturday, 6=Sunday
    
    # First API call 
    try:
        response = openai_client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"  # we let LLM decide when to use tools
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        
        # If LLM wants to use tools
        if tool_calls:
            # Add LLM's response to messages
            messages.append(response_message)
            
            # Execute each tool call
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 Calling tool: {function_name}")
                print(f"📝 Arguments: {function_args}")
                
                # Get the function
                function_to_call = available_functions.get(function_name)
                
                if function_to_call:
                    # Special handling for functions that need is_weekend
                    if function_name == "suggest_activities" and "is_weekend" not in function_args:
                        function_args["is_weekend"] = is_weekend
                    
                    # Execute the function
                    try:
                        function_response = function_to_call(**function_args)
                        print(f"✅ Result: {function_response}\n")
                    except Exception as e:
                        function_response = {"success": False, "error": str(e)}
                        print(f"❌ Error: {e}\n")
                else:
                    function_response = {"success": False, "error": f"Function {function_name} not found"}
                
                # Add function result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": json.dumps(function_response)
                })
            
            # Second API call - let LLM use the tool results
            second_response = openai_client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
            
            return second_response.choices[0].message.content
        
        else:
            # No tools needed, return text response
            return response_message.content
    
    except Exception as e:
        return f"❌ Sorry, I encountered an error: {str(e)}\n\nPlease try again or rephrase your question."




# Create Gradio Interface
with gr.Blocks(title="Weather Activity Planner", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown("""
    # 🌤️ Weather-Based Activity Planner
    ### Your Personal Weather Assistant & Activity Recommender
    
    Ask me about:
    - 🌡️ Current weather in any city
    - 📅 Weather forecasts for the next 5 days
    - 🎯 Activity suggestions based on weather
    - ☔ Whether you need an umbrella
    - 📆 Best day for outdoor activities
    - 🧥 What to wear based on conditions
    
    **Powered by real-time weather data from OpenWeatherMap API**
    """)
    
    chatbot = gr.ChatInterface(
        fn=chat_with_tools,
        type="messages",
        examples=[
            "What's the weather like in Paris today?",
            "What should I do this weekend in London?",
            "Will I need an umbrella in Tokyo this week?",
            "What's the best day to visit New York in the next 5 days?",
            "Is it a good day for outdoor activities in Berlin?",
            "What's the weather forecast for Barcelona?",
            "Should I bring a jacket to Amsterdam today?",
            "Compare weather in Paris vs London today"
        ],
        cache_examples=False,
        title="",
        description="",
    )
    
    gr.Markdown("""
    ---
    ### 💡 Tips:
    - Mention specific cities for accurate weather data
    - Ask about multiple days ahead for forecast
    - Request activity suggestions for personalized recommendations
    - Specify Fahrenheit if you prefer (default is Celsius)
    
    ### 🌍 Supported Cities:
    Works with any major city worldwide! Examples: Paris, New York, Tokyo, London, Sydney, Dubai, Mumbai...
    
    ### ⚙️ Features:
    - ✅ Real-time weather data
    - ✅ 5-day forecasts
    - ✅ Smart activity suggestions
    - ✅ Comfort index calculation
    - ✅ Best day recommendations
    - ✅ Weather-appropriate tips
    
    ### 🔧 Tools Used:
    This assistant uses multiple AI tools to:
    1. Fetch real weather data from OpenWeatherMap API
    2. Analyze weather conditions
    3. Calculate comfort indices
    4. Generate personalized activity suggestions
    5. Find optimal days for activities
    """)


if __name__ == "__main__":
    # Check if API keys are set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in .env file")
        exit(1)
    
    if not os.getenv("OPENWEATHERMAP_API_KEY"):
        print("❌ Error: OPENWEATHERMAP_API_KEY not found in .env file")
        exit(1)
    
    print("✅ API keys loaded successfully")
    print("🚀 Launching Weather Activity Planner...")
    print("📍 Once launched, try asking: 'What should I do in Paris today?'\n")
    
    demo.launch()