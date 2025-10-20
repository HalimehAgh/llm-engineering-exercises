"""
Gradio Web Interface for Multimodal AI Assistant
Provides an interactive chat interface with image display
"""

import gradio as gr
from agent import chat, start_conversation, add_user_message

# Global settings
ENABLE_VOICE = True
ENABLE_IMAGE = True


def process_message(message, history):
    """
    Process a user message and get AI response
    
    Args:
        message (str): User's input message
        history (list): Conversation history in Gradio format
    
    Returns:
        tuple: ("", updated_history, image_or_none)
    """
    if not message.strip():
        return "", history, None
    
    # Add user message to history
    history = add_user_message(history, message)
    
    # Get AI response with potential image
    try:
        updated_history, image = chat(
            history,
            enable_voice=ENABLE_VOICE,
            enable_image=ENABLE_IMAGE
        )
        return "", updated_history, image
    
    except Exception as e:
        # On error, show error message
        error_msg = f"❌ Error: {str(e)}"
        history.append({"role": "assistant", "content": error_msg})
        return "", history, None


def clear_conversation():
    """
    Clear the conversation and image
    
    Returns:
        tuple: (empty_history, None)
    """
    return start_conversation(), None


# Create the Gradio interface
with gr.Blocks(title="Multimodal AI Travel Assistant", theme=gr.themes.Soft()) as demo:
    
    # Header
    gr.Markdown("""
    # 🌍 Multimodal AI Travel Assistant
    
    An intelligent assistant that can:
    - 💬 Answer questions about cities and destinations
    - 🎨 Generate beautiful images of cities
    - 🔊 Speak responses aloud
    
    **Try asking:** "Show me Paris" or "Tell me about Tokyo"
    """)
    
    # Main layout: Chat on left, Image on right
    with gr.Row():
        with gr.Column(scale=1):
            chatbot = gr.Chatbot(
                label="Conversation",
                type="messages",
                height=500,
                avatar_images=(None, "🤖")
            )
        
        with gr.Column(scale=1):
            image_output = gr.Image(
                label="Generated Image",
                height=500,
                type="pil"
            )
    
    # Input area
    with gr.Row():
        message_input = gr.Textbox(
            label="Your Message",
            placeholder="Type your message here... (e.g., 'Show me Paris')",
            scale=4
        )
        send_button = gr.Button("Send", variant="primary", scale=1)
    
    # Control buttons
    with gr.Row():
        clear_button = gr.Button("🗑️ Clear Conversation")
        
        # Settings (could be expanded later)
        with gr.Column():
            gr.Markdown("ℹ️ **Voice and image generation are enabled by default**")
    
    # Example prompts
    gr.Examples(
        examples=[
            "Show me Paris",
            "I'm planning a trip to Tokyo. Can you show me what it looks like?",
            "Tell me about Rome",
            "Show me New York City in cyberpunk style",
            "What's the best time to visit London?",
        ],
        inputs=message_input,
        label="💡 Example Prompts"
    )
    
    # Event handlers
    
    # Send message on button click
    send_button.click(
        fn=process_message,
        inputs=[message_input, chatbot],
        outputs=[message_input, chatbot, image_output]
    )
    
    # Send message on Enter key
    message_input.submit(
        fn=process_message,
        inputs=[message_input, chatbot],
        outputs=[message_input, chatbot, image_output]
    )
    
    # Clear conversation
    clear_button.click(
        fn=clear_conversation,
        inputs=None,
        outputs=[chatbot, image_output]
    )
    
    # Footer
    gr.Markdown("""
    ---
    **Built with:** OpenAI GPT-4, DALL-E 3, TTS | **Framework:** Gradio
    
    """)


if __name__ == "__main__":
    """
    Launch the Gradio interface
    """
    demo.launch(
        server_name="127.0.0.1",  # localhost
        server_port=7860,          # default Gradio port
        share=False,               # set to True to get a public URL
        inbrowser=True             # automatically open in browser
    )