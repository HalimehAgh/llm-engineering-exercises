# Exercise 6: Multimodal AI Travel Assistant

An AI assistant that combines language models, image generation, and voice synthesis to create an engaging travel planning experience.

## 🎯 Overview

This project demonstrates a multimodal AI system with **agentic capabilities** - the AI autonomously decides when to use tools based on conversation context. Built as part of my LLM Engineering learning journey.

### Key Capabilities

- **💬 Intelligent Conversation**: Powered by GPT-4 for natural dialogue
- **🎨 Autonomous Image Generation**: AI decides when to generate city images using DALL-E 3
- **🔊 Voice Synthesis**: Speaks responses using OpenAI TTS
- **🌐 Web Interface**: Clean, interactive Gradio interface

## 🏗️ Architecture

### Agentic Framework

The system uses an **agentic pattern** where the AI:
1. Analyzes user requests
2. Decides if tools are needed
3. Executes appropriate tools
4. Generates contextual responses

```
User Input → Agent (GPT-4) → Decision
                               ↓
                    Tool Needed? → Yes → Execute Tool → Generate Response
                               ↓
                               No → Direct Response
```

### Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | GPT-4 | Conversation and decision-making |
| **Image Generation** | DALL-E 3 | Create city visualizations |
| **Voice Synthesis** | OpenAI TTS | Text-to-speech output |
| **UI** | Gradio | Web interface |
| **Image Processing** | Pillow | Image handling |

## 🚀 Installation

### Prerequisites

- Python 3.11+
- OpenAI API key
- FFmpeg (for audio processing)

### Step 1: Clone the Repository

```bash
git clone https://github.com/HalimehAgh/llm-engineering-exercises.git
cd llm-engineering-exercises/exercises/exercise-6-multimodal-ai-assistant
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install FFmpeg

**Windows:**
1. Download: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
2. Extract to `C:\ffmpeg\`
3. Add `C:\ffmpeg\bin` to System PATH
4. Restart terminal

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update && sudo apt install ffmpeg
```

### Step 4: Configure API Key

Create a `.env` file:

```bash
OPENAI_API_KEY=your_api_key_here
```

## 💻 Usage

### Launch the Web Interface

```bash
python src/ui.py
```

The interface will open automatically at `http://localhost:7860`


Potential additions:
- [ ] Support for multiple simultaneous tools
- [ ] Image editing and variations
- [ ] Speech-to-text for voice input
- [ ] Conversation history persistence
- [ ] RAG for factual accuracy
- [ ] Multi-language support
- [ ] Additional tools (weather, news, etc.)
- [ ] User authentication



---