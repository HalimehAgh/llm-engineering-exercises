"""
Tool Definitions for the AI Agent
Defines what tools are available to the AI and their schemas
"""

# Tool definitions in OpenAI function calling format
tools = [
    {
        "type": "function",
        "function": {
            "name": "generate_city_image",
            "description": (
                "Generate a vibrant pop-art style image of a city showing "
                "tourist attractions, landmarks, and unique features. "
                "Use this when the user asks to see a city, wants a visual "
                "representation, or is planning to visit a destination."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": (
                            "The name of the city to visualize. "
                            "Examples: 'Paris', 'Tokyo', 'New York City'"
                        )
                    },
                    "style": {
                        "type": "string",
                        "description": (
                            "The art style for the image. "
                            "Default is 'vibrant pop-art'. "
                            "Other options: 'watercolor', 'cyberpunk', 'vintage'"
                        ),
                        "default": "vibrant pop-art"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# System message that defines the AI's behavior
system_message = """You are a helpful and enthusiastic travel assistant with multimodal capabilities.

Your role:
- Help users learn about cities and travel destinations
- Provide interesting facts and travel information
- Generate beautiful visualizations of cities when appropriate
- Be conversational, friendly, and engaging

When to use the generate_city_image tool:
- User asks to "see" or "show" a city
- User asks "what does [city] look like"
- User is planning to visit and wants visual inspiration
- User asks about tourist attractions or landmarks
- The conversation would benefit from a visual representation

When NOT to use the tool:
- User asks about weather, prices, or factual data
- User asks for travel tips without requesting visuals
- Questions about booking, flights, or logistics
- General conversation not related to city visualization

Guidelines:
- Be concise but informative
- After generating an image, describe what's shown briefly
- Encourage exploration and ask follow-up questions
- Maintain context from previous messages in the conversation
- Don't generate multiple images in a single response
"""

# Model configuration
MODEL = "gpt-4o"  # or "gpt-4-turbo", "gpt-3.5-turbo"


def get_tools():
    """
    Returns the list of available tools
    
    Returns:
        list: Tool definitions for OpenAI API
    """
    return tools


def get_system_message():
    """
    Returns the system message for the AI agent
    
    Returns:
        str: System message defining AI behavior
    """
    return system_message


def get_model():
    """
    Returns the model name to use
    
    Returns:
        str: OpenAI model name
    """
    return MODEL


if __name__ == "__main__":
    """
    Display tool configuration
    """
    import json
    
    print("=" * 60)
    print("TOOL CONFIGURATION")
    print("=" * 60)
    
    print("\n📋 Available Tools:")
    for tool in tools:
        func = tool["function"]
        print(f"\n  • {func['name']}")
        print(f"    Description: {func['description'][:80]}...")
        print(f"    Parameters: {list(func['parameters']['properties'].keys())}")
        print(f"    Required: {func['parameters'].get('required', [])}")
    
    print("\n" + "=" * 60)
    print("SYSTEM MESSAGE")
    print("=" * 60)
    print(system_message)
    
    print("\n" + "=" * 60)
    print(f"MODEL: {MODEL}")
    print("=" * 60)