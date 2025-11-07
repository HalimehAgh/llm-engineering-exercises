# Gmail RAG Assistant

Ask questions about your Gmail emails using Retrieval Augmented Generation (RAG).

## Features

- OAuth2 Gmail authentication
- Semantic search through your emails using OpenAI embeddings
- Natural language question answering with GPT-4o-mini
- Conversational interface with Gradio
- Source citations for transparency

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=your_key_here
```

3. Set up Google Cloud credentials:
   - Create a project at [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Gmail API
   - Create OAuth 2.0 credentials (Desktop app)
   - Download and save as `credentials.json`

4. Run the app:
```bash
python gmail_rag_assistant.py
```

## Usage

1. **Authenticate** with your Gmail account
2. **Load emails** (start with 10-50 for testing)
3. **Ask questions** like:
   - "What are my recent emails about?"
   - "Do I have any meeting invites?"
   - "Summarize emails from LinkedIn"

## Tech Stack

- **LangChain** - RAG orchestration
- **FAISS** - Vector database
- **OpenAI** - Embeddings & LLM (GPT-4o-mini)
- **Gradio** - Web interface
- **Gmail API** - Email access

