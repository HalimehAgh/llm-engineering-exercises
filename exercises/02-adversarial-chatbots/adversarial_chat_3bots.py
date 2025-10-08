"""
Adversarial Conversation between 3 Chatbots
GPT (argumentative), Claude (polite), and Gemini (neutral moderator)
"""
from openai import OpenAI
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
google_client = OpenAI (api_key=GOOGLE_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")  

# Model names
gpt_model = "gpt-4o-mini"
claude_model = "claude-3-haiku-20240307"
gemini_model = "gemini-2.0-flash-exp"

#System prompts
gpt_system = """You are a chatbot who is very argumentative; 
you disagree with anything in the conversation and you challenge everything, in a snarky way."""

claude_system = """You are a very polite, courteous chatbot. You try to agree with 
everything the other person says, or find common ground. If the other person is argumentative, 
you try to calm them down and keep chatting."""

gemini_system = """You are a neutral, wise moderator in this conversation. 
You try to find middle ground between different viewpoints, summarize key points, 
and keep the conversation productive. You're diplomatic and balanced."""

# Conversation history
gpt_messages = ["Hi everyone, ready to debate!"]
claude_messages = ["Hello everyone, lovely to meet all!"]
gemini_messages = ["Greetings! Let's have a throughtful discussion."]

def call_gpt():
    """Generate GPT's response based on conversation history.  """
    messages=[
        {"role": "system", "content": gpt_system}]
    for gpt_msg, claude_msg, gemini_msg in zip(gpt_messages, claude_messages, gemini_messages):
        messages.append({"role": "assistant", "content": gpt_msg})
        messages.append({"role": "user", "content": f"Claude: {claude_msg}"})
        messages.append({"role": "user", "content": f"Gemini: {gemini_msg}"})

        completion = openai_client.chat.completions.create(
            model=gpt_model,
            messages=messages,
            max_tokens=500
        )
    return completion.choices[0].message.content

def call_claude():
    """Generate Claude's response based on conversation history.  """
    messages=[]
        
    for gpt_msg, claude_msg, gemini_msg in zip(gpt_messages, claude_messages, gemini_messages):
        messages.append({"role": "assistant", "content": claude_msg})
        messages.append({"role": "user", "content": f"GPT: {gpt_msg}"})
        messages.append({"role": "user", "content": f"Gemini: {gemini_msg}"})

     # Add latest messages from the others (GPT just responded)
    messages.append({"role": "user", "content": f"GPT: {gpt_messages[-1]}"})
    message=anthropic_client.messages.create(
       model=claude_model,    
       max_tokens=500,
       system=claude_system,
       messages=messages
    )
    return message.content[0].text

def call_gemini():
    """Generate Gemini's response based on conversation history.  """
    messages=[
        {"role": "system", "content": gemini_system}]
    for gpt_msg, claude_msg, gemini_msg in zip(gpt_messages, claude_messages, gemini_messages):
        messages.append({"role": "assistant", "content": gemini_msg})
        messages.append({"role": "user", "content": f"GPT: {gpt_msg}"})
        messages.append({"role": "user", "content": f"Claude: {claude_msg}"})

     # Add latest messages from the others (GPT and Claude just responded)
    if len(gpt_messages) > len(gemini_messages):
        messages.append({"role": "user", "content": f"GPT: {gpt_messages[-1]}"})
    if len(claude_messages) > len(gemini_messages):
        messages.append({"role": "user", "content": f"Claude: {claude_messages[-1]}"})
    # Call Gemini via OpenAI API    
    completion = google_client.chat.completions.create(
        model=gemini_model,
        messages=messages,
        max_tokens=500
    )
    return completion.choices[0].message.content

def main():
    """Run the 3-way adversarial conversation"""
    print("=" * 80)
    print("THREE-WAY ADVERSARIAL CHATBOT CONVERSATION")
    print("GPT (Argumentative) vs Claude (Polite) vs Gemini (Moderator)")
    print("=" * 80)

    print(f"\n💬 GPT: {gpt_messages[0]}")
    print(f"\n💬 Claude: {claude_messages[0]}")
    print(f"\n💬 Gemini: {gemini_messages[0]}")

    num_rounds = 5
    for round_num in range(1, num_rounds + 1):
        print(f"\n{'='*80}")
        print(f"ROUND {round_num}")
        print(f"{'='*80}")

        # GPT's turn
        print("\nGPT is thinking...")
        try:
            gpt_next=call_gpt()
            gpt_messages.append(gpt_next)
            print(f"\n💬 GPT: \n{gpt_next}")
        except Exception as e:
            print("❌ Error calling GPT:", e)
            break

        # Claude's turn
        print("\nClaude is thinking...")
        try:
            claude_next=call_claude()
            claude_messages.append(claude_next)
            print(f"\n💬 Claude: \n{claude_next}")
        except Exception as e:
            print("❌ Error calling Claude:", e)
            break

        # Gemini's turn
        print("\nGemini is thinking...")
        try:
            gemini_next=call_gemini()
            gemini_messages.append(gemini_next)
            print(f"\n💬 Gemini: \n{gemini_next}")
        except Exception as e:
            print("❌ Error calling Gemini:", e)
            break

    print(f"\n{'='*80}")
    print("Conversation ended.")
    print(f"Total messages: GPT={len(gpt_messages)}, Claude={len(claude_messages)}, Gemini={len(gemini_messages)}")
    print('='*80)

if __name__ == "__main__":
    main()
