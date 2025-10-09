# Exercise 04: Smart Shopping Assistant

## 🎯 Overview
An intelligent AI shopping assistant that provides personalized shopping help with dynamic context awareness. The assistant adapts its responses based on customer needs, preferences, inventory status, and conversation context.

## ✨ Features

### Dynamic Context Injection
The assistant intelligently adjusts responses based on:

1. **📦 Inventory Status**
   - Out of stock items → Apologize and suggest alternatives
   - New arrivals → Extra enthusiasm and details
   - Sale items → Natural emphasis on deals

2. **💬 Customer Intent Recognition**
   - Budget concerns → Focus on value and sales
   - Special occasions → Ask detailed questions
   - Uncertainty → Extra guidance and questions
   - Gift shopping → Thoughtful recipient questions

3. **🎨 Preference Detection**
   - Color mentions → Personalized suggestions
   - Size concerns → Sizing advice
   - Style preferences → Tailored recommendations

4. **😊 Sentiment Awareness**
   - Positive feedback → Shared excitement
   - Negative experiences → Empathy and extra care
   - Compliments → Reinforcement and upselling

### Store Configuration
Easy-to-modify store settings:
```python
STORE_CONFIG = {
    "sales": {...},           # Current promotions
    "out_of_stock": [...],    # Unavailable items
    "new_arrivals": [...],    # Trending items
    "premium_items": [...]    # High-end products
}