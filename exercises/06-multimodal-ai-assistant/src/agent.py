"""
AI Agent with Agentic Framework
Handles conversation flow and autonomous tool usage
"""

import openai
import os
import json
from dotenv import load_dotenv

from tools import get_tools, get_system_message, get_model
from image_generator import generate_city_image
from voice_generator import text_to_speech

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def handle_tool_call(message):
    """
    Execute a tool call requested by the AI
    
    Args:
        message: The assistant message containing tool_calls
    
    Returns:
        tuple: (tool_response_message, city_name)
            - tool_response_message: Message to send back to AI
            - city_name: The city extracted from the tool call
    """
    # Get the first tool call (we only expect one at a time)
    tool_call = message.tool_calls[0]
    
    # Extract function name and arguments
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    print(f"\n🔧 Tool called: {function_name}")
    print(f"📝 Arguments: {arguments}")
    
    # Extract city and style (with default)
    city = arguments.get("city")
    style = arguments.get("style", "vibrant pop-art")
    
    # Create the response message for the AI
    # This tells the AI that the tool was executed successfully
    tool_response = {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": function_name,
        "content": f"Successfully generated a {style} style image of {city}"
    }
    
    return tool_response, city, style


def chat(history, enable_voice=True, enable_image=True):
    """
    Main chat function with agentic capabilities
    
    Args:
        history (list): List of conversation messages with roles
        enable_voice (bool): Whether to speak responses
        enable_image (bool): Whether to generate images
    
    Returns:
        tuple: (updated_history, image_or_none)
            - updated_history: Conversation history with new response
            - image_or_none: PIL Image if generated, None otherwise
    """
    # Prepare messages: system message + conversation history
    messages = [{"role": "system", "content": get_system_message()}] + history
    
    # Initial AI request with tools
    print("\n💭 Asking AI...")
    response = openai.chat.completions.create(
        model=get_model(),
        messages=messages,
        tools=get_tools() if enable_image else None
    )
    
    # Initialize image as None
    image = None
    
    # Check if AI wants to use a tool
    if response.choices[0].finish_reason == "tool_calls":
        print("🎯 AI decided to use a tool!")
        
        # Extract the assistant's message with tool call
        assistant_message = response.choices[0].message
        
        # Execute the tool
        tool_response, city, style = handle_tool_call(assistant_message)
        
        # Add both messages to conversation history
        messages.append({
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in assistant_message.tool_calls
            ]
        })
        messages.append(tool_response)
        
        # Actually generate the image if enabled
        if enable_image:
            try:
                print(f"\n🎨 Generating image of {city}...")
                image = generate_city_image(city, style=style)
                print("✅ Image generated!")
            except Exception as e:
                print(f"❌ Image generation failed: {e}")
                # Update tool response to reflect failure
                tool_response["content"] = f"Failed to generate image: {str(e)}"
        
        # Get AI's final response after tool execution
        print("\n💭 Getting AI's final response...")
        response = openai.chat.completions.create(
            model=get_model(),
            messages=messages
        )
    
    # Extract the text reply
    reply = response.choices[0].message.content
    print(f"\n🤖 AI: {reply[:100]}...")
    
    # Add assistant's reply to history
    history.append({"role": "assistant", "content": reply})
    
    # Speak the response if enabled
    if enable_voice:
        try:
            print("\n🔊 Speaking response...")
            text_to_speech(reply, filename="response.mp3")
        except Exception as e:
            print(f"⚠️  Voice generation failed: {e}")
    
    return history, image


def start_conversation():
    """
    Start a new conversation
    
    Returns:
        list: Empty conversation history
    """
    return []


def add_user_message(history, message):
    """
    Add a user message to the conversation history
    
    Args:
        history (list): Current conversation history
        message (str): User's message
    
    Returns:
        list: Updated history
    """
    history.append({"role": "user", "content": message})
    return history


if __name__ == "__main__":
    """
    Test the agent in console mode
    """
    print("=" * 60)
    print("MULTIMODAL AI TRAVEL ASSISTANT")
    print("=" * 60)
    print("\nType 'quit' to exit")
    print("Try: 'Show me Paris' or 'Tell me about Tokyo'\n")
    
    # Start conversation
    history = start_conversation()
    
    # Simple console loop
    while True:
        # Get user input
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add user message
        history = add_user_message(history, user_input)
        
        # Get AI response
        try:
            history, image = chat(
                history,
                enable_voice=True,
                enable_image=True
            )
            
            # Show image if generated
            if image:
                print("\n🖼️  Displaying image...")
                image.show()
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            # Remove the last user message if there was an error
            history = history[:-1]