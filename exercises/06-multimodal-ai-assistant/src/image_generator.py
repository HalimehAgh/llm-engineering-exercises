"""
Image Generation Module
Uses OpenAI's DALL-E 3 to generate city images
"""

import openai
import base64
from io import BytesIO
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_city_image(city, style="vibrant pop-art", size="1024x1024", quality="standard"):
    """
    Generate an image of a city using DALL-E 3
    
    Args:
        city (str): Name of the city
        style (str): Art style for the image (default: "vibrant pop-art")
        size (str): Image size - "1024x1024", "1792x1024", or "1024x1792"
        quality (str): Image quality - "standard" or "hd"
    
    Returns:
        PIL.Image: Generated image object
    
    Raises:
        Exception: If image generation fails
    """
    try:
        print(f"🎨 Generating image for {city}...")
        
        # Create the prompt
        prompt = (
            f"An image representing a vacation in {city}, "
            f"showing tourist spots and everything unique about {city}, "
            f"in a {style} style"
        )
        
        # Call DALL-E 3 API
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
            response_format="b64_json",  # Get base64 encoded image
        )
        
        # Extract base64 image data
        image_base64 = response.data[0].b64_json
        
        # Decode base64 to bytes
        image_data = base64.b64decode(image_base64)
        
        # Create PIL Image object from bytes
        image = Image.open(BytesIO(image_data))
        
        print(f"✅ Image generated successfully!")
        return image
        
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        raise


def save_image(image, filename="output.png"):
    """
    Save a PIL Image to a file
    
    Args:
        image (PIL.Image): Image to save
        filename (str): Output filename
    """
    try:
        image.save(filename)
        print(f"💾 Image saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving image: {e}")



if __name__ == "__main__":
    """
    Test the image generator
    """
    print("Testing Image Generator...")
    print("-" * 50)
    
    # Test 1: Generate Paris image
    try:
        paris_img = generate_city_image("Paris")
        paris_img.show()  # Display the image
        save_image(paris_img, "paris_test.png")
    except Exception as e:
        print(f"Test failed: {e}")
    
    # Test 2: Generate with different style
    print("\n" + "-" * 50)
    try:
        tokyo_img = generate_city_image("Tokyo", style="cyberpunk neon")
        tokyo_img.show()
        save_image(tokyo_img, "tokyo_test.png")
    except Exception as e:
        print(f"Test failed: {e}")