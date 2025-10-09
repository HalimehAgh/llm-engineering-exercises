"""
Smart Content Rewriter
Takes any text and rewrites it in multiple styles simultaneously.
Perfect for social media, marketing, and professional communication.
"""

from openai import OpenAI
import anthropic
import os
from dotenv import load_dotenv
import gradio as gr

# Load environment variables
load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Model names
gpt_model = "gpt-4o-mini"
claude_model = "claude-3-haiku-20240307"


def rewrite_with_gpt(content, style_prompt):
    """Rewrite content using GPT"""
    try:
        response = openai_client.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": "You are an expert content writer who adapts text to different styles and formats."},
                {"role": "user", "content": f"{style_prompt}\n\nOriginal content:\n{content}"}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"


def rewrite_with_claude(content, style_prompt):
    """Rewrite content using Claude"""
    try:
        message = claude_client.messages.create(
            model=claude_model,
            system="You are an expert content writer who adapts text to different styles and formats.",
            messages=[
                {"role": "user", "content": f"{style_prompt}\n\nOriginal content:\n{content}"}
            ],
            max_tokens=1000
        )
        return message.content[0].text
    except Exception as e:
        return f"❌ Error: {str(e)}"


def rewrite_content(content, model_choice):
    """
    Rewrite content in 5 different styles
    Returns a dictionary with all versions
    """
    
    if not content.strip():
        return {
            "professional": "⚠️ Please enter some content to rewrite.",
            "casual": "⚠️ Please enter some content to rewrite.",
            "tweet": "⚠️ Please enter some content to rewrite.",
            "linkedin": "⚠️ Please enter some content to rewrite.",
            "summary": "⚠️ Please enter some content to rewrite."
        }
    
    # Choose rewrite function based on model
    rewrite_fn = rewrite_with_claude if model_choice == "Claude" else rewrite_with_gpt
    
    # Define style prompts
    styles = {
        "professional": """Rewrite this in a professional, formal business tone. 
Use sophisticated vocabulary, proper grammar, and maintain a serious, corporate voice. 
Keep it concise and clear.""",
        
        "casual": """Rewrite this in a casual, friendly, conversational tone. 
Use simple words, contractions, and write like you're talking to a friend. 
Keep it relaxed and approachable.""",
        
        "tweet": """Convert this into a compelling Twitter/X thread (max 3 tweets). 
Each tweet must be under 280 characters. Use emojis, hashtags, and make it engaging. 
Format as Tweet 1, Tweet 2, etc.""",
        
        "linkedin": """Rewrite this as a LinkedIn post. 
Start with a hook, use line breaks for readability, include relevant emojis sparingly, 
and end with a call-to-action or question to drive engagement. Keep it professional but personable.""",
        
        "summary": """Create a concise summary of this content. 
Extract only the key points in 2-3 bullet points. Be extremely brief and clear."""
    }
    
    # Generate all versions
    results = {}
    for style_name, style_prompt in styles.items():
        results[style_name] = rewrite_fn(content, style_prompt)
    
    return results


def process_rewrite(content, model):
    """
    Process the rewrite and return formatted results for Gradio
    """
    yield {
        professional_out: "⏳ Generating professional version...",
        casual_out: "",
        tweet_out: "",
        linkedin_out: "",
        summary_out: ""
    }
    
    results = rewrite_content(content, model)
    
    # Yield results one by one for a nice effect
    yield {
        professional_out: results["professional"],
        casual_out: "⏳ Generating casual version...",
        tweet_out: "",
        linkedin_out: "",
        summary_out: ""
    }
    
    yield {
        professional_out: results["professional"],
        casual_out: results["casual"],
        tweet_out: "⏳ Generating tweet thread...",
        linkedin_out: "",
        summary_out: ""
    }
    
    yield {
        professional_out: results["professional"],
        casual_out: results["casual"],
        tweet_out: results["tweet"],
        linkedin_out: "⏳ Generating LinkedIn post...",
        summary_out: ""
    }
    
    yield {
        professional_out: results["professional"],
        casual_out: results["casual"],
        tweet_out: results["tweet"],
        linkedin_out: results["linkedin"],
        summary_out: "⏳ Generating summary..."
    }
    
    # Final result
    yield {
        professional_out: results["professional"],
        casual_out: results["casual"],
        tweet_out: results["tweet"],
        linkedin_out: results["linkedin"],
        summary_out: results["summary"]
    }


# Create Gradio Interface
with gr.Blocks(title="Smart Content Rewriter", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown("""
    # ✍️ Smart Content Rewriter
    ### Transform your content into multiple styles instantly!
    
    Paste any text and get 5 different versions:
    - 📊 **Professional** - Formal business tone
    - 💬 **Casual** - Friendly and conversational  
    - 🐦 **Tweet Thread** - Twitter-ready with emojis
    - 💼 **LinkedIn Post** - Engagement-optimized
    - 📝 **Summary** - Key points only
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            content_input = gr.Textbox(
                label="Original Content",
                placeholder="Paste your text here...\n\nExample: I'm excited to announce that our company just launched a new AI-powered tool that helps businesses automate their customer service. This tool uses advanced language models to understand customer queries and provide accurate responses.",
                lines=10
            )
            
            model_choice = gr.Radio(
                choices=["GPT", "Claude"],
                label="Select AI Model",
                value="Claude"
            )
            
            rewrite_btn = gr.Button("✨ Rewrite Content", variant="primary", size="lg")
            
            gr.Markdown("""
            ---
            💡 **Tips:**
            - Works best with 50-500 words
            - Can rewrite blog posts, emails, announcements, etc.
            - Try both models to compare results!
            """)
        
        with gr.Column(scale=2):
            with gr.Tabs():
                with gr.Tab("📊 Professional"):
                    professional_out = gr.Textbox(
                        label="Professional Version",
                        lines=8,
                        show_copy_button=True
                    )
                
                with gr.Tab("💬 Casual"):
                    casual_out = gr.Textbox(
                        label="Casual Version",
                        lines=8,
                        show_copy_button=True
                    )
                
                with gr.Tab("🐦 Tweet Thread"):
                    tweet_out = gr.Textbox(
                        label="Tweet Thread",
                        lines=8,
                        show_copy_button=True
                    )
                
                with gr.Tab("💼 LinkedIn"):
                    linkedin_out = gr.Textbox(
                        label="LinkedIn Post",
                        lines=8,
                        show_copy_button=True
                    )
                
                with gr.Tab("📝 Summary"):
                    summary_out = gr.Textbox(
                        label="Summary",
                        lines=8,
                        show_copy_button=True
                    )
    
    # Example content
    gr.Examples(
        examples=[
            ["We're thrilled to announce the launch of our new AI-powered analytics platform. This innovative solution helps businesses make data-driven decisions faster than ever before. Our platform integrates seamlessly with existing tools and provides real-time insights.", "Claude"],
            ["I just finished reading an amazing book about artificial intelligence and its impact on society. The author discusses both the opportunities and challenges that AI brings to our world. It really made me think about the future.", "GPT"],
            ["Our team has been working hard on improving customer satisfaction. We've implemented new training programs, upgraded our support systems, and hired additional staff. The results have been outstanding with a 40% increase in positive feedback.", "Claude"]
        ],
        inputs=[content_input, model_choice],
        label="Try these examples:"
    )
    
    # Connect button to function
    rewrite_btn.click(
        fn=process_rewrite,
        inputs=[content_input, model_choice],
        outputs=[professional_out, casual_out, tweet_out, linkedin_out, summary_out]
    )


if __name__ == "__main__":
    demo.launch()