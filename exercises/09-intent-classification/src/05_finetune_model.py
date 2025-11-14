import openai
import os
import time
import json
from datetime import datetime


openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("⚠️  Please set your OPENAI_API_KEY environment variable!")
    print("   export OPENAI_API_KEY='your-key-here'")
    exit(1)

print("="*60)
print("GPT-4o-mini Fine-tuning for Intent Classification")
print("="*60)

# Step 1: Upload training file
print("\n📤 Step 1: Uploading training file...")
with open("data/openai_format/train.jsonl", "rb") as f:
    training_file = openai.files.create(
        file=f,
        purpose="fine-tune"
    )
print(f"✅ Training file uploaded: {training_file.id}")

# Step 2: Upload validation file
print("\n📤 Step 2: Uploading validation file...")
with open("data/openai_format/validation.jsonl", "rb") as f:
    validation_file = openai.files.create(
        file=f,
        purpose="fine-tune"
    )
print(f"✅ Validation file uploaded: {validation_file.id}")

# Step 3: Create fine-tuning job
print("\n🚀 Step 3: Creating fine-tuning job...")
print(f"   Model: gpt-4o-mini-2024-07-18")
print(f"   Epochs: 1")
print(f"   Estimated cost: ~$0.82")

fine_tune_job = openai.fine_tuning.jobs.create(
    training_file=training_file.id,
    validation_file=validation_file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={
        "n_epochs": 1
    },
    suffix="intent-classifier"  # Model will be named: ft:gpt-4o-mini:...:intent-classifier
)

print(f"✅ Fine-tuning job created: {fine_tune_job.id}")
print(f"   Status: {fine_tune_job.status}")

# Step 4: Monitor training progress
print("\n⏳ Step 4: Monitoring training progress...")
print("   (This may take 10-20 minutes)")

start_time = time.time()
while True:
    job = openai.fine_tuning.jobs.retrieve(fine_tune_job.id)
    status = job.status
    
    elapsed = int(time.time() - start_time)
    print(f"   [{elapsed}s] Status: {status}")
    
    if status == "succeeded":
        print("\n🎉 Fine-tuning completed successfully!")
        break
    elif status == "failed":
        print("\n❌ Fine-tuning failed!")
        print(f"   Error: {job.error}")
        exit(1)
    elif status == "cancelled":
        print("\n⚠️  Fine-tuning was cancelled")
        exit(1)
    
    time.sleep(30)  # Check every 30 seconds

# Step 5: Get fine-tuned model info
fine_tuned_model_id = job.fine_tuned_model
print(f"\n✅ Fine-tuned model ID: {fine_tuned_model_id}")

# Step 6: Save model info
model_info = {
    "fine_tuned_model_id": fine_tuned_model_id,
    "base_model": "gpt-4o-mini-2024-07-18",
    "training_file_id": training_file.id,
    "validation_file_id": validation_file.id,
    "job_id": fine_tune_job.id,
    "n_epochs": 1,
    "created_at": datetime.now().isoformat(),
    "status": job.status,
    "trained_tokens": job.trained_tokens if hasattr(job, 'trained_tokens') else None
}

os.makedirs('models', exist_ok=True)
with open('models/model_info.json', 'w') as f:
    json.dump(model_info, f, indent=2)

print(f"\n✅ Model info saved: models/model_info.json")

# Step 7: View training results
print("\n📊 Training Results:")
if hasattr(job, 'result_files') and job.result_files:
    print(f"   Result files: {job.result_files}")
    print("   💡 View detailed metrics in OpenAI dashboard:")
    print(f"   https://platform.openai.com/finetune/{fine_tune_job.id}")

