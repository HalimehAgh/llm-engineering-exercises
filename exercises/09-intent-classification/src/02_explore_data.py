from datasets import load_dataset
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
dataset = load_dataset("clinc_oos", "plus")

# Get intent names
intent_names = dataset['train'].features['intent'].names

# Count samples per intent
train_intent_counts = Counter(dataset['train']['intent'])
val_intent_counts = Counter(dataset['validation']['intent'])
test_intent_counts = Counter(dataset['test']['intent'])

print("="*60)
print("CLINC150 DATASET EXPLORATION")
print("="*60)

# Basic stats
print(f"\n📊 Dataset Size:")
print(f"Training samples: {len(dataset['train'])}")
print(f"Validation samples: {len(dataset['validation'])}")
print(f"Test samples: {len(dataset['test'])}")
print(f"Number of intents: {len(intent_names)}")

# Class distribution statistics
train_counts = list(train_intent_counts.values())
print(f"\n⚖️ Class Distribution (Training Set):")
print(f"Min samples per intent: {min(train_counts)}")
print(f"Max samples per intent: {max(train_counts)}")
print(f"Average samples per intent: {np.mean(train_counts):.1f}")
print(f"Median samples per intent: {np.median(train_counts):.1f}")

# Check if balanced
if min(train_counts) == max(train_counts):
    print("✅ Dataset is PERFECTLY balanced!")
else:
    print(f"⚠️ Dataset is imbalanced (range: {max(train_counts) - min(train_counts)})")

# Text length analysis
train_lengths = [len(text.split()) for text in dataset['train']['text']]
print(f"\n📏 Text Length Statistics (words):")
print(f"Average: {np.mean(train_lengths):.1f}")
print(f"Min: {min(train_lengths)}")
print(f"Max: {max(train_lengths)}")
print(f"Median: {np.median(train_lengths):.1f}")

# Sample intents with examples
print(f"\n🏷️ Sample Intent Categories:")
for i in range(10):
    intent_name = intent_names[i]
    # Get one example
    examples = [ex['text'] for ex in dataset['train'] if ex['intent'] == i]
    print(f"\n{i+1}. {intent_name} ({len(examples)} samples)")
    print(f"   Example: '{examples[0]}'")

# Visualizations
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Plot 1: Samples per intent (histogram)
axes[0, 0].hist(train_counts, bins=20, edgecolor='black')
axes[0, 0].set_xlabel('Number of Samples')
axes[0, 0].set_ylabel('Number of Intents')
axes[0, 0].set_title('Distribution of Samples Across Intents')
axes[0, 0].axvline(np.mean(train_counts), color='red', linestyle='--', 
                    label=f'Mean: {np.mean(train_counts):.0f}')
axes[0, 0].legend()

# Plot 2: Text length distribution
axes[0, 1].hist(train_lengths, bins=30, edgecolor='black', alpha=0.7)
axes[0, 1].set_xlabel('Text Length (words)')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].set_title('Distribution of Text Lengths')
axes[0, 1].axvline(np.mean(train_lengths), color='red', linestyle='--',
                    label=f'Mean: {np.mean(train_lengths):.1f}')
axes[0, 1].legend()

# Plot 3: Train/Val/Test split
split_sizes = [len(dataset['train']), len(dataset['validation']), len(dataset['test'])]
axes[1, 0].bar(['Train', 'Validation', 'Test'], split_sizes, 
                color=['blue', 'green', 'orange'])
axes[1, 0].set_ylabel('Number of Samples')
axes[1, 0].set_title('Dataset Splits')
for i, v in enumerate(split_sizes):
    axes[1, 0].text(i, v + 200, str(v), ha='center', fontweight='bold')

# Plot 4: Top 20 intents by sample count
top_20_intents = train_intent_counts.most_common(20)
intent_labels = [intent_names[i] for i, _ in top_20_intents]
counts = [c for _, c in top_20_intents]
y_pos = np.arange(len(intent_labels))
axes[1, 1].barh(y_pos, counts)
axes[1, 1].set_yticks(y_pos)
axes[1, 1].set_yticklabels(intent_labels, fontsize=8)
axes[1, 1].set_xlabel('Number of Samples')
axes[1, 1].set_title('Top 20 Most Common Intents')
axes[1, 1].invert_yaxis()

plt.tight_layout()
plt.savefig('clinc150_exploration.png', dpi=300, bbox_inches='tight')
print("\n✅ Visualization saved: clinc150_exploration.png")
plt.show()

print("\n" + "="*60)
print("RECOMMENDATION:")
print("="*60)
if min(train_counts) == max(train_counts):
    print("✅ Dataset is balanced - we can use all samples as-is!")
else:
    print(f"💡 Consider balancing to {min(train_counts)} samples per intent")
    print(f"   This would give us: {len(intent_names)} × {min(train_counts)} = {len(intent_names) * min(train_counts)} training samples")