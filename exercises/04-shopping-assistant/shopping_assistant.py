"""
Smart Shopping Assistant
An AI shopping asssistant that adapts responses based on:
- Current sales and promotions
- Customer preferences
- Inventory availability
- Conversation context
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# Load environment variables
load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

STORE_CONFIG = {
    "name": "StyleHub",
    "sales": {
        "hats": 60,
        "shirts": 50,
        "pants": 50,
        "jackets": 30,
        "dresses": 40
    },
    "out_of_stock": ["belts", "scarves", "ties"],
    "new_arrivals": ["sneakers", "sunglasses", "backpacks"],
    "premium_items": ["leather jackets", "designer jeans", "watches"]
}

def create_base_system_message():
    sales_list= "\n".join([f"-{item.capitalize()}: {discount}% off" for item, discount in STORE_CONFIG["sales"].items()])
    return f"""You are a friendly, enthusiastic shopping assistant at {STORE_CONFIG['name']}, a modern clothing store.

    Your personality:
    - Warm and approachable
    - Genuinely helpful, not pushy
    - Knowledgeable about fashion
    - Excited about helping customers find perfect items

    Your goals:
    1. Understand customer needs through questions
    2. Suggest appropriate items (with subtle emphasis on sale items)
    3. Provide honest styling advice
    4. Make shopping experience delightful

    🎉 Current Sales:
    {sales_list}

    Example interactions:

    Customer: "I need something for a job interview"
    You: "Wonderful! A job interview is such an exciting opportunity! For a polished, professional look, I'd recommend our dress shirts - and great timing, they're {STORE_CONFIG['sales']['shirts']}% off right now! 

    What industry is the interview in? That'll help me suggest the perfect style - classic and conservative, or modern and creative?"

    Customer: "Do you have casual clothes?"
    You: "Absolutely! We have fantastic casual options. Our casual shirts and pants are both on sale at {STORE_CONFIG['sales']['pants']}% off! 

    Are you building a complete casual wardrobe, or looking for specific pieces to mix and match?"

    Customer: "What's trending right now?"
    You: "Great question! Right now we're seeing lots of interest in our new arrivals - especially {STORE_CONFIG['new_arrivals'][0]} and {STORE_CONFIG['new_arrivals'][1]}! They're flying off the shelves!

    What's your usual style - more classic and timeless, or do you like staying on top of the latest trends?"

    Important rules:
    - Always be honest - if something won't work, say so kindly
    - Ask questions to understand needs before suggesting items
    - When items are on sale, mention it naturally (not aggressively)
    - Be enthusiastic but authentic
    - Use emojis sparingly for warmth (1-2 per response max)"""

def chat(message, history):
    """
    Main chat function with dynamic context injection
    """
    system_context = create_base_system_message()

    for item in STORE_CONFIG["out_of_stock"]:
        if item in message.lower():
            system_context+= f"\n\n⚠️ IMPORTANT: We don't have {item} in stock right now. Apologize sincerely, explain we're restocking soon, and enthusiastically suggest similar items that ARE available and on sale."
    
    for item in STORE_CONFIG["premium_items"]:
        if item in message.lower():
            system_context+= f"\n\n💎 Customer is interested in premium items ({item}). Emphasize quality, craftsmanship, longevity, and value. These are investments, not just purchases."
    
    for item in STORE_CONFIG["new_arrivals"]:
        if item in message.lower():
            system_context+= f"\n\n✨ GREAT! Customer asked about {item} which are new arrivals! Be extra enthusiastic, mention they're trending, describe features, and ask about their style preferences."
    
    if any(word in message.lower() for word in ['budget', 'cheap', 'affordable', 'expensive', 'price', 'cost', 'save', 'deal']):
        system_context+= "\n\n💰 Customer is price-conscious! Emphasize sale items enthusiastically, talk about value and quality, mention 'great deal' and 'investment pieces'. Focus on items with highest discounts first."
    occasions = ['wedding', 'interview', 'date', 'party', 'funeral', 'graduation', 'birthday']
    
    for occasion in occasions:
        if occasion in message.lower():
            system_context += f"\n\n🎉 Customer needs outfit for {occasion}! Ask thoughtful questions: dress code? venue? season? their personal style? Then suggest complete outfit with confidence."
   
    if any(phrase in message.lower() for phrase in ['not sure', 'maybe', 'thinking', 'undecided', "don't know", 'help me decide']):
        system_context += "\n\n🤔 Customer seems uncertain. Be extra patient and helpful. Ask guiding questions about: preferred colors, typical style, comfort vs fashion, occasion. Offer to narrow down options together."
   
    if any(word in message.lower() for word in ['size', 'fit', 'too big', 'too small', 'tight', 'loose']):
        system_context += "\n\n📏 Customer has size/fit concerns. Ask about their usual size, fit preferences (slim/regular/relaxed), and offer sizing advice. Mention our easy return/exchange policy."
    
    colors = ['black', 'white', 'red', 'blue', 'green', 'yellow', 'pink', 'purple', 'brown', 'gray', 'navy']
    mentioned_colors = [color for color in colors if color in message.lower()]
    if mentioned_colors:
        system_context += f"\n\n🎨 Customer mentioned {', '.join(mentioned_colors)}! Use this to personalize suggestions. Ask if they want matching items or complementary colors."
    
    if any(phrase in message.lower() for phrase in ["didn't like", "wasn't good", "disappointed", "not happy", "bad experience"]):
        system_context += "\n\n😔 Customer had a negative experience. Be empathetic, apologize if appropriate, and work extra hard to make this experience better. Ask what went wrong to avoid suggesting similar items."

    if any(word in message.lower() for word in ['love', 'perfect', 'great', 'amazing', 'exactly', 'thank you', 'thanks']):
        system_context += "\n\n😊 Customer is happy! Share their excitement! This is going well. Ask if they need anything else to complete their look or if they'd like to see similar items."

    item_count= sum(1 for item in STORE_CONFIG["sales"] if item in message.lower())
    if item_count >=2:
        system_context += "\n\n🛍️ Customer mentioned multiple items. Help them prioritize based on their needs. Ask: 'What's most urgent?' or 'Shall we start with [item] and then move to [item]?"
    
    if any(word in message.lower() for word in ['gift', 'present', 'birthday', 'anniversary', 'christmas', 'mother', 'father', 'friend']):
        system_context += "\n\n🎁 Customer is gift shopping! Ask about recipient: age? style? relationship? occasion? Budget? Then suggest thoughtful options. Mention gift wrapping if available."

# Build conversation with history
    messages = [
        {"role": "system", "content": system_context}
    ] + history + [
        {"role": "user", "content": message}
    ]
    stream=openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.8,
        stream=True
    )
    response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            response += content
            yield response

#Create Gradio interface
with gr.Blocks(title="StyleHub Shopping Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🛍️ StyleHub Shopping Assistant
    ### Your Personal AI Shopping Companion
    
    Welcome to StyleHub! I'm here to help you find the perfect items. 
    Whether you're looking for something specific or just browsing, let's chat!
    
    💡 **Current Promotions:**
    - 🎩 Hats: 60% OFF
    - 👔 Shirts: 50% OFF  
    - 👖 Pants: 50% OFF
    - 🧥 Jackets: 30% OFF
    - 👗 Dresses: 40% OFF
    """)
    chatbot=gr.ChatInterface(
        fn=chat,
        type="messages",
        examples=["I need an outfit for a job interview next week",
            "Do you have any belts?",
            "What's on sale today?",
            "I'm looking for casual clothes but I'm on a tight budget",
            "I want something stylish for a first date",
            "Do you have sneakers? What colors?",
            "I need a gift for my dad's birthday",
            "Not sure what I need, just want to look good"
        ],
        cache_examples=False,
    )

    gr.Markdown("""
    ---
    ### 💡 Tips for Best Experience:
    - Tell me about the occasion or your style preferences
    - Mention your budget if you have one
    - Ask about specific items or let me help you discover options
    - I'm here to help - no question is too small!
    
    ### 🏪 Store Features:
    - ✨ New arrivals weekly
    - 💰 Frequent sales and promotions  
    - 📦 Easy returns and exchanges
    - 🎁 Gift wrapping available
    """)

if __name__ == "__main__":
    demo.launch()

    
