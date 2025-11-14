from datasets import load_dataset

# CLINC150 - 150 intent classification
dataset = load_dataset("clinc_oos", "plus")

# Print dataset info
print("Dataset structure:")
print(dataset)
print("\nTraining samples:", len(dataset['train']))
print("Validation samples:", len(dataset['validation']))
print("Test samples:", len(dataset['test']))

# Show few examples
print("\nFirst 3 examples:")
for i in range(3):
    example = dataset['train'][i]
    print(f"\nText: {example['text']}")
    print(f"Intent: {example['intent']}")

print("\n✅ Dataset downloaded and ready!")