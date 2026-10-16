# Smart Multimodal Visual Rag

Visual RAG agent that parses PDFs with layout, tables and images (Docling + Poppler) and answers questions over both text and visuals.

**Tech:** Python, Docling, LangChain, vision-language models

## Run it

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main_agent.py
```

API keys are read from environment variables. Copy `.env.example` to `.env` and fill in your own keys.

Install Poppler separately (https://github.com/oschwartz10612/poppler-windows) and add it to PATH. Put your own PDFs next to the script to test.

---
By [Muhammad Ali](https://muhammad773-bit.github.io), BS Artificial Intelligence, SMIU Karachi.
