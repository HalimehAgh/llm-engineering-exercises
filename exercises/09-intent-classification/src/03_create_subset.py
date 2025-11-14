from datasets import load_dataset, Dataset, DatasetDict
from collections import Counter
import random
import json
import os

random.seed(42)

dataset = load_dataset("clinc_oos", "plus")

intent_names = dataset['train'].features['intent'].names

SAMPLES_PER_INTENT = 50

def balance_dataset(dataset_split, samples_per_intent):
    """Balance dataset to have equal samples per intent"""
    balanced_data = {'text': [], 'intent': []}
    
    all_intents = set(dataset_split['intent'])
    
    for intent in sorted(all_intents):
        # Get all samples for this intent
        intent_samples = [(ex['text'], ex['intent']) 
                         for ex in dataset_split 
                         if ex['intent'] == intent]
        
        # Sample up to desired amount (or all if less available)
        n_samples = min(samples_per_intent, len(intent_samples))
        sampled = random.sample(intent_samples, n_samples)
        
        # Add to balanced dataset
        balanced_data['text'].extend([s[0] for s in sampled])
        balanced_data['intent'].extend([s[1] for s in sampled])
        
        print(f"Intent {intent:3d} ({intent_names[intent]:30s}): {len(intent_samples):3d} → {n_samples:3d} samples")
    
    return balanced_data

# Balance each split
print(f"\n{'='*60}")
print("Balancing training set...")
print(f"{'='*60}")
train_balanced = balance_dataset(dataset['train'], SAMPLES_PER_INTENT)

print(f"\n{'='*60}")
print("Balancing validation set...")
print(f"{'='*60}")
val_balanced = balance_dataset(dataset['validation'], SAMPLES_PER_INTENT // 5)  # 10 samples per intent

print(f"\n{'='*60}")
print("Balancing test set...")
print(f"{'='*60}")
test_balanced = balance_dataset(dataset['test'], SAMPLES_PER_INTENT // 2)  # 25 samples per intent

# Create dataset dict
balanced_dataset = DatasetDict({
    'train': Dataset.from_dict(train_balanced),
    'validation': Dataset.from_dict(val_balanced),
    'test': Dataset.from_dict(test_balanced)
})

# Print final statistics
print(f"\n{'='*60}")
print("FINAL SUBSET STATISTICS")
print(f"{'='*60}")
print(f"Training samples: {len(balanced_dataset['train'])}")
print(f"Validation samples: {len(balanced_dataset['validation'])}")
print(f"Test samples: {len(balanced_dataset['test'])}")
print(f"Total samples: {len(balanced_dataset['train']) + len(balanced_dataset['validation']) + len(balanced_dataset['test'])}")

# Verify balance
train_intent_counts = Counter(balanced_dataset['train']['intent'])
print(f"\n⚖️ Balance Check:")
print(f"Min samples per intent: {min(train_intent_counts.values())}")
print(f"Max samples per intent: {max(train_intent_counts.values())}")
print(f"Average samples per intent: {sum(train_intent_counts.values()) / len(train_intent_counts):.1f}")

# Save metadata
metadata = {
    'total_intents': len(intent_names),
    'samples_per_intent_train': SAMPLES_PER_INTENT,
    'samples_per_intent_val': SAMPLES_PER_INTENT // 5,
    'samples_per_intent_test': SAMPLES_PER_INTENT // 2,
    'train_samples': len(balanced_dataset['train']),
    'val_samples': len(balanced_dataset['validation']),
    'test_samples': len(balanced_dataset['test']),
    'intent_names': intent_names,
    'random_seed': 42
}

print("\n✅ Balanced subset created successfully!")

# Show sample of balanced data
print(f"\n{'='*60}")
print("Sample from balanced training set:")
print(f"{'='*60}")
for i in range(5):
    example = balanced_dataset['train'][i]
    print(f"\nText: {example['text']}")
    print(f"Intent: {intent_names[example['intent']]}")

# ============================================================
# SAVE BALANCED DATASET TO DISK
# ============================================================

# Create directory for balanced subset
os.makedirs('data/balanced_subset', exist_ok=True)

print(f"\n{'='*60}")
print("Saving balanced subset to disk...")
print(f"{'='*60}")

# Save train set
with open('data/balanced_subset/train.json', 'w', encoding='utf-8') as f:
    json.dump(train_balanced, f, indent=2, ensure_ascii=False)
print("✅ Saved: data/balanced_subset/train.json")

# Save validation set
with open('data/balanced_subset/validation.json', 'w', encoding='utf-8') as f:
    json.dump(val_balanced, f, indent=2, ensure_ascii=False)
print("✅ Saved: data/balanced_subset/validation.json")

# Save test set
with open('data/balanced_subset/test.json', 'w', encoding='utf-8') as f:
    json.dump(test_balanced, f, indent=2, ensure_ascii=False)
print("✅ Saved: data/balanced_subset/test.json")

# Save intent name mapping
with open('data/balanced_subset/intent_names.json', 'w', encoding='utf-8') as f:
    json.dump({'intent_names': intent_names}, f, indent=2)
print("✅ Saved: data/balanced_subset/intent_names.json")

# Save metadata
with open('data/balanced_subset/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
print("✅ Saved: data/balanced_subset/metadata.json")

