"""
Voice Generation Module
Uses OpenAI's TTS API to convert text to speech
"""

import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def text_to_speech(text, voice="onyx", model="tts-1", filename="speech.mp3", autoplay=True):
    """
    Convert text to speech using OpenAI TTS
    
    Args:
        text (str): Text to convert to speech
        voice (str): Voice to use - options: alloy, echo, fable, onyx, nova, shimmer
        model (str): Model to use - "tts-1" (faster) or "tts-1-hd" (higher quality)
        filename (str): Output filename for the audio
        autoplay (bool): Whether to play the audio automatically (Windows only)
    
    Returns:
        str: Path to the saved audio file
    
    Raises:
        Exception: If TTS generation fails
    """
    try:
        print(f"🔊 Generating speech: '{text[:50]}...'")
        
        # Call OpenAI TTS API
        response = openai.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        
        # Save audio to file
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Audio saved to {filename}")
        
        # Auto-play on Windows
        if autoplay:
            try:
                os.startfile(filename)
                print(f"▶️  Playing audio...")
            except AttributeError:
                # Not on Windows
                print(f"💡 Play the audio file manually: {filename}")
        
        return filename
        
    except Exception as e:
        print(f"❌ Error generating speech: {e}")
        raise


def generate_speech_silent(text, voice="onyx", model="tts-1", filename="speech.mp3"):
    """
    Generate speech without auto-playing
    
    Args:
        text (str): Text to convert to speech
        voice (str): Voice to use
        model (str): TTS model
        filename (str): Output filename
    
    Returns:
        str: Path to the saved audio file
    """
    return text_to_speech(text, voice, model, filename, autoplay=False)




if __name__ == "__main__":
    """
    Test the voice generator
    """
    print("Testing Voice Generator...")
    print("-" * 50)
    
    # Test 1: Simple message
    print("\n📝 Test 1: Simple greeting")
    try:
        text_to_speech("Well, hi there!")
        print("✅ Test 1 passed")
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
    
    # Test 2: Different voices
    print("\n📝 Test 2: Different voices")
    voices = ["alloy", "echo", "nova"]
    
    for voice in voices:
        try:
            print(f"\nTesting voice: {voice}")
            text_to_speech(
                f"Hello, I am {voice}",
                voice=voice,
                filename=f"test_{voice}.mp3",
                autoplay=False
            )
            print(f"✅ {voice} voice test passed")
        except Exception as e:
            print(f"❌ {voice} voice test failed: {e}")
    
    # Test 3: Longer text
    print("\n📝 Test 3: Longer text")
    long_text = """
    Paris is the capital and most populous city of France. 
    Known as the City of Light, it's famous for its art, fashion, 
    and culture. The Eiffel Tower is its most iconic landmark.
    """
    try:
        text_to_speech(long_text, filename="paris_description.mp3", autoplay=False)
        print("✅ Test 3 passed")
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
    
    print("\n" + "=" * 50)
    print("All tests completed!")