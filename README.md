# 🔒 Secure Local Enterprise AI Pipeline (RAG Gateway)

An enterprise-ready, zero-cloud knowledge retrieval ecosystem designed to bridge generative AI capabilities with strict corporate data governance and security frameworks. 

## 🚀 Architectural Overview
This system intercepts user requests via an interactive web interface, evaluates inputs against modern threat signatures, references an isolated local vector database for information retrieval, and securely prompts a local inference model—keeping 100% of data within the enterprise perimeter.

### 🛡️ Core Features
*   **AI Guardroom (Input Sanitization):** Mitigates OWASP Top 10 for LLM vulnerabilities by executing real-time signature matching for prompt injection attempts.
*   **Data Leakage Prevention (PII Redaction):** Utilizes regex parsing engines to scrub sensitive corporate identifiers (Emails, IP Addresses) prior to vector tokenization.
*   **Context Isolation (RAG Database):** Leverages `ChromaDB` as an in-memory vector store, ensuring semantic search queries are restricted to authorized enterprise parameters.
*   **Local Inference Engine:** Integrates `Ollama` hosting Meta's `Llama 3.2 (1B)` model locally, removing reliance on external cloud APIs and guaranteeing total data sovereignty.

## 🛠️ Tech Stack
*   **Language:** Python 3.12
*   **Database:** ChromaDB (Vector Storage)
*   **AI Engine:** Ollama (Llama 3.2)
*   **Interface:** Streamlit Dashboard

## 🔧 Installation & Setup
1. Clone the repository and install requirements:
   ```bash
   pip install chromadb streamlit
   ```
2. Download and initialize the local inference model:
   ```bash
   ollama run llama3.2:1b
   ```
3. Boot the application layer:
   ```bash
   streamlit run app.py
   ```
