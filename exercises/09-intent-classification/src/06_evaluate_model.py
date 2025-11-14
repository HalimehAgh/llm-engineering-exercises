import openai
import json
import os
from collections import Counter
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import wandb
from tqdm import tqdm

# Get API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load model info
print("Loading model info...")
with open('models/model_info.json', 'r') as f:
    model_info = json.load(f)

fine_tuned_model_id = model_info['fine_tuned_model_id']
print(f"✅ Model ID: {fine_tuned_model_id}")

# Load test data
print("\nLoading test data...")
test_data = []
with open('data/openai_format/test.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        test_data.append(json.loads(line))

print(f"✅ Test samples: {len(test_data)}")

# Load intent names
with open('data/balanced_subset/intent_names.json', 'r', encoding='utf-8') as f:
    intent_names = json.load(f)['intent_names']


# Initialize Wandb in offline mode (no server sync needed)
print("\n🚀 Initializing Weights & Biases (offline mode)...")
os.environ["WANDB_MODE"] = "offline"
wandb.init(
    project="intent-classification-gpt4o-mini",
    name="gpt4o-mini-clinc150-evaluation",
    config={
        "model": "gpt-4o-mini-2024-07-18",
        "fine_tuned_model_id": fine_tuned_model_id,
        "dataset": "CLINC150-balanced",
        "n_epochs": 1,
        "num_intents": len(intent_names),
        "test_samples": len(test_data)
    }
)
print("✅ Wandb initialized (offline - results saved locally)")

# Run predictions
print("\n🔮 Running predictions on test set...")

predictions = []
true_labels = []
failed_predictions = 0

for i, sample in enumerate(tqdm(test_data)):
    messages = sample['messages']
    true_intent = messages[-1]['content']  # Assistant's response is the true intent
    
    try:
        # Get prediction from fine-tuned model
        response = openai.chat.completions.create(
            model=fine_tuned_model_id,
            messages=messages[:-1],  # Don't include the assistant's answer
            temperature=0,
            max_tokens=10
        )
        
        predicted_intent = response.choices[0].message.content.strip()
        predictions.append(predicted_intent)
        true_labels.append(true_intent)
        
    except Exception as e:
        print(f"\n⚠️  Error on sample {i}: {e}")
        failed_predictions += 1
        predictions.append("UNKNOWN")
        true_labels.append(true_intent)

print(f"\n✅ Predictions complete!")
print(f"   Failed predictions: {failed_predictions}")

print("\n📊 Calculating metrics...")

accuracy = accuracy_score(true_labels, predictions)

intent_to_id = {name: i for i, name in enumerate(intent_names)}
true_ids = [intent_to_id.get(label, -1) for label in true_labels]
pred_ids = [intent_to_id.get(pred, -1) for pred in predictions]

# Filter out unknown predictions
valid_indices = [i for i, (t, p) in enumerate(zip(true_ids, pred_ids)) if t != -1 and p != -1]
true_ids_valid = [true_ids[i] for i in valid_indices]
pred_ids_valid = [pred_ids[i] for i in valid_indices]

macro_f1 = f1_score(true_ids_valid, pred_ids_valid, average='macro', zero_division=0)
micro_f1 = f1_score(true_ids_valid, pred_ids_valid, average='micro', zero_division=0)
precision = precision_score(true_ids_valid, pred_ids_valid, average='weighted', zero_division=0)
recall = recall_score(true_ids_valid, pred_ids_valid, average='weighted', zero_division=0)

# Print results
print("\n" + "="*60)
print("EVALUATION RESULTS")
print("="*60)
print(f"Accuracy:           {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"Macro F1 Score:     {macro_f1:.4f}")
print(f"Micro F1 Score:     {micro_f1:.4f}")
print(f"Precision:          {precision:.4f}")
print(f"Recall:             {recall:.4f}")
print(f"Failed predictions: {failed_predictions}/{len(test_data)}")

# Log to Wandb
wandb.log({
    "accuracy": accuracy,
    "macro_f1": macro_f1,
    "micro_f1": micro_f1,
    "precision": precision,
    "recall": recall,
    "failed_predictions": failed_predictions
})

# Create confusion matrix (top 20 intents for readability)
print("\n📊 Creating confusion matrix...")
top_intents = [name for name, _ in Counter(true_labels).most_common(20)]
top_intent_ids = [intent_to_id[name] for name in top_intents]

# Filter for top intents
top_indices = [i for i, t in enumerate(true_ids_valid) if t in top_intent_ids]
true_top = [true_ids_valid[i] for i in top_indices]
pred_top = [pred_ids_valid[i] for i in top_indices]

if len(true_top) > 0:
    cm = confusion_matrix(true_top, pred_top, labels=top_intent_ids)
    
    plt.figure(figsize=(15, 12))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=top_intents, yticklabels=top_intents,
                cbar_kws={'label': 'Count'})
    plt.title('Confusion Matrix (Top 20 Intents)')
    plt.xlabel('Predicted Intent')
    plt.ylabel('True Intent')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    # Save locally
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    print("✅ Confusion matrix saved: confusion_matrix.png")
    
    # Log to Wandb
    wandb.log({"confusion_matrix": wandb.Image('confusion_matrix.png')})

# Classification report
print("\n📋 Classification Report (Top 20 intents):")
if len(true_top) > 0:
    report = classification_report(
        true_top, 
        pred_top, 
        labels=top_intent_ids,  
        target_names=top_intents,
        zero_division=0
    )
    print(report)

# Error analysis
print("\n🔍 Error Analysis (Sample mistakes):")
mistakes = [(t, p) for t, p in zip(true_labels, predictions) if t != p][:10]
for i, (true_intent, pred_intent) in enumerate(mistakes[:5], 1):
    print(f"\n{i}. True: {true_intent}")
    print(f"   Predicted: {pred_intent}")

# Save results
results = {
    "model_id": fine_tuned_model_id,
    "accuracy": float(accuracy),
    "macro_f1": float(macro_f1),
    "micro_f1": float(micro_f1),
    "precision": float(precision),
    "recall": float(recall),
    "failed_predictions": failed_predictions,
    "total_samples": len(test_data),
    "num_intents": len(intent_names)
}

os.makedirs('results', exist_ok=True)
with open('results/evaluation_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n✅ Results saved: results/evaluation_results.json")

# Log final summary to Wandb
wandb.summary["final_accuracy"] = accuracy
wandb.summary["final_f1"] = macro_f1

print("\n" + "="*60)
print("✅ EVALUATION COMPLETE!")
print("="*60)
print(f"\n🎯 Accuracy: {accuracy*100:.2f}%")
print(f"📊 View detailed metrics in Wandb dashboard")

wandb.finish()