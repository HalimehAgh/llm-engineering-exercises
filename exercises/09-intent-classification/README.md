# Intent Classification with Fine-tuned GPT-4o-mini

A complete LLM engineering project demonstrating end-to-end fine-tuning of OpenAI's GPT-4o-mini model for multi-class intent classification on the CLINC150 dataset.

## 🎯 Project Overview

This project fine-tunes GPT-4o-mini to classify user queries into 151 different intent categories across 10 domains (banking, travel, utility, work, etc.). The model achieves **96.79% accuracy** on the test set.

### Key Achievements

- ✅ **96.79% accuracy** on 151-class classification
- ✅ **98.03% macro F1-score** - excellent balance across all classes
- ✅ **Cost-efficient**: Total fine-tuning cost < $1
- ✅ **Balanced dataset**: 50 samples per intent for fair training
- ✅ **Zero failed predictions** on 3,775 test samples

## 📊 Results

| Metric | Score |
|--------|-------|
| Accuracy | 96.79% |
| Macro F1 | 98.03% |
| Micro F1 | 98.20% |
| Precision | 98.27% |
| Recall | 98.20% |

![Confusion Matrix](confusion_matrix.png)

## 🗂️ Project Structure
```
09-intent-classification/
├── data/
│   ├── balanced_subset/           # Curated balanced dataset
│   │   ├── train.json             # 7,550 samples
│   │   ├── validation.json        # 1,510 samples
│   │   ├── test.json              # 3,775 samples
│   │   ├── intent_names.json      # 151 intent labels
│   │   └── metadata.json          # Dataset statistics
│   └── openai_format/             # OpenAI fine-tuning format
│       ├── train.jsonl
│       ├── validation.jsonl
│       └── test.jsonl
├── src/
│   ├── 01_download_data.py        # Download CLINC150 dataset
│   ├── 02_explore_data.py         # Data visualization & analysis
│   ├── 03_create_subset.py        # Create balanced subset
│   ├── 04_prepare_openai_format.py # Convert to JSONL format
│   ├── 05_finetune_model.py       # Fine-tune GPT-4o-mini
│   └── 07_evaluate_model.py       # Model evaluation
├── models/
│   └── model_info.json            # Fine-tuned model metadata
├── results/
│   └── evaluation_results.json    # Evaluation metrics
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
OpenAI API key
Weights & Biases account (optional, for tracking)
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/HalimehAgh/llm-engineering-exercises.git
cd llm-engineering-exercises/exercises/09-intent-classification
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export WANDB_API_KEY="your-wandb-api-key"  # Optional
```

## 📝 Usage

### Step 1: Download and Explore Dataset
```bash
# Download CLINC150 dataset
python src/01_download_data.py

# Explore and visualize data
python src/02_explore_data.py
```

### Step 2: Create Balanced Subset
```bash
# Create balanced subset (50 samples per intent)
python src/03_create_subset.py
```

**Rationale:** Original dataset has 15,250 samples across 151 intents. We created a balanced subset to:
- Reduce training costs
- Prevent class imbalance
- Maintain all 151 intents for comprehensive coverage

### Step 3: Prepare Data for Fine-tuning
```bash
# Convert to OpenAI JSONL format
python src/04_prepare_openai_format.py
```

### Step 4: Fine-tune Model
```bash
# Fine-tune GPT-4o-mini (1 epoch, ~20 minutes)
python src/05_finetune_model.py
```

**Configuration:**
- Base model: `gpt-4o-mini-2024-07-18`
- Epochs: 1
- Training samples: 7,550
- Validation samples: 1,510

### Step 5: Evaluate Model
```bash
# Evaluate on test set and generate metrics
python src/07_evaluate_model.py
```

Outputs:
- Accuracy, F1, Precision, Recall
- Confusion matrix visualization
- Classification report
- Error analysis


## 🔍 Dataset Details

### CLINC150
- **Source:** [PolyAI/clinc_oos](https://huggingface.co/datasets/clinc_oos)
- **Domains:** Banking, Travel, Utility, Work, Auto & Commute, Kitchen & Dining, Home, Meta, Small Talk, Credit Cards
- **Total Intents:** 151 (150 in-scope + 1 out-of-scope)
- **Task:** Multi-class text classification

### Balanced Subset Statistics
```
Training:    7,550 samples (50 per intent)
Validation:  1,510 samples (10 per intent)
Test:        3,775 samples (25 per intent)
```

### Sample Intents

| Intent | Example Query |
|--------|--------------|
| `transfer` | "I want to send money to my friend" |
| `balance` | "What's my account balance?" |
| `book_flight` | "I need to book a flight to Paris" |
| `weather` | "What's the weather like in London?" |

## 📈 Model Performance

### Accuracy by Domain (Top Performers)

The model performs exceptionally well across all domains, with particularly strong performance in:
- Banking operations (97-99% accuracy)
- Travel queries (96-98% accuracy)
- General utility queries (95-97% accuracy)

### Error Analysis

- **Total mistakes:** 121 out of 3,775 (3.21%)
- **Common confusions:** Semantically similar intents (e.g., "transfer" vs "pay_bill")
- **No systematic failures** across any particular domain

## 🛠️ Technical Details

### Fine-tuning Configuration
```python
{
  "model": "gpt-4o-mini-2024-07-18",
  "n_epochs": 1,
  "learning_rate_multiplier": "auto",
  "batch_size": "auto"
}
```

### Evaluation Metrics

- **Accuracy:** Exact match between predicted and true intent
- **Macro F1:** Unweighted average F1 across all classes
- **Micro F1:** Global average accounting for class imbalance
- **Confusion Matrix:** Top 20 most common intents visualized

## 📚 Key Learnings

1. **Dataset Balancing:** Balanced datasets significantly improve multi-class performance
2. **Cost Optimization:** Strategic data curation and prompt engineering reduce costs by ~95%
3. **Few Epochs Suffice:** With quality data, 1 epoch can achieve excellent results
4. **Prompt Engineering:** Minimal system prompts work well for fine-tuned models
5. **Evaluation is Critical:** Comprehensive metrics reveal model strengths/weaknesses

## 🔮 Future Improvements

- [ ] Compare with open-source models (DistilBERT, RoBERTa)
- [ ] Experiment with different epoch counts (2-3 epochs)
- [ ] Add few-shot examples in system prompt for edge cases
- [ ] Deploy as API endpoint for real-time inference
- [ ] Test on out-of-domain queries
- [ ] Upload balanced dataset to Hugging Face

## 🙏 Acknowledgments

- **Dataset:** [CLINC150](https://github.com/clinc/oos-eval) by Larson et al. (2019)
- **Platform:** OpenAI GPT-4o-mini API
- **Tracking:** Weights & Biases

## 📄 Citation
```bibtex
@inproceedings{larson-etal-2019-evaluation,
    title = "An Evaluation Dataset for Intent Classification and Out-of-Scope Prediction",
    author = "Larson, Stefan and Mahendran, Anish and Peper, Joseph J. and 
              Clarke, Christopher and Lee, Andrew and Hill, Parker and 
              Kummerfeld, Jonathan K. and Leach, Kevin and 
              Laurenzano, Michael A. and Tang, Lingjia and Mars, Jason",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in 
                 Natural Language Processing",
    year = "2019"
}
```

## 📧 Contact

**Your Name**
- GitHub: [@HalimehAgh](https://github.com/YOUR_USERNAME)
- LinkedIn: [Halimeh Agh](https://www.linkedin.com/in/halimeh-agh-83071049/)
- Email: agh.halime@gmail.com

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**⭐ If you found this project helpful, please consider giving it a star!**