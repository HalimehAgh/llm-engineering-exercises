import json
import os

# Load balanced subset
print("Loading balanced subset...")
with open('data/balanced_subset/train.json', 'r', encoding='utf-8') as f:
    train_data = json.load(f)

with open('data/balanced_subset/validation.json', 'r', encoding='utf-8') as f:
    val_data = json.load(f)

with open('data/balanced_subset/test.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

with open('data/balanced_subset/intent_names.json', 'r', encoding='utf-8') as f:
    intent_names = json.load(f)['intent_names']

print(f"Train samples: {len(train_data['text'])}")
print(f"Validation samples: {len(val_data['text'])}")
print(f"Test samples: {len(test_data['text'])}")

# Create system message
SYSTEM_MESSAGE = "You are an intent classification assistant. Classify the user query into the appropriate intent category."

# Convert to OpenAI format
def convert_to_openai_format(data, intent_names):
    """Convert our format to OpenAI's messages format"""
    openai_format = []
    
    for text, intent_id in zip(data['text'], data['intent']):
        intent_name = intent_names[intent_id]
        
        openai_format.append({
            "messages": [
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": text},
                {"role": "assistant", "content": intent_name}
            ]
        })
    
    return openai_format

print("\nConverting to OpenAI format...")
train_openai = convert_to_openai_format(train_data, intent_names)
val_openai = convert_to_openai_format(val_data, intent_names)
test_openai = convert_to_openai_format(test_data, intent_names)

# Create directory
os.makedirs('data/openai_format', exist_ok=True)

# Save as JSONL
print("\nSaving JSONL files...")
with open('data/openai_format/train.jsonl', 'w', encoding='utf-8') as f:
    for item in train_openai:
        f.write(json.dumps(item) + '\n')
print(f"✅ Saved: data/openai_format/train.jsonl ({len(train_openai)} samples)")

with open('data/openai_format/validation.jsonl', 'w', encoding='utf-8') as f:
    for item in val_openai:
        f.write(json.dumps(item) + '\n')
print(f"✅ Saved: data/openai_format/validation.jsonl ({len(val_openai)} samples)")

with open('data/openai_format/test.jsonl', 'w', encoding='utf-8') as f:
    for item in test_openai:
        f.write(json.dumps(item) + '\n')
print(f"✅ Saved: data/openai_format/test.jsonl ({len(test_openai)} samples)")

# Show sample
print("\n" + "="*60)
print("Sample training example:")
print("="*60)
print(json.dumps(train_openai[0], indent=2))
