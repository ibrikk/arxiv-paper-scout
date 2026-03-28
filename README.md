# arxiv-paper-scout (Starter Template)

AI-powered research paper analyzer - workshop edition.

## Quick Setup

```bash
# 1. Create virtual environment
uv venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\Activate.ps1  # Windows

# 2. Install dependencies
uv pip install -r requirements.txt

# 3. Configure API key
cp .env.example .env
# Edit .env and add your Groq API key

# 4. Run
python main.py

Get Your API Key
Go to https://console.groq.com/keys
Sign up (free)
Create new API key
Paste into .env file
Workshop Goals
By the end, you'll understand:

 What LangChain is and why it's useful
 How to get structured JSON from LLMs (not messy text)
 What RAG (Retrieval Augmented Generation) means
 How to chain multiple LLM calls together