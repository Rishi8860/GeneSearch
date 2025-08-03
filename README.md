# 🧬 GeneSearch — LLM-powered ACMG Attribute Classifier

GeneSearch is a natural language search engine for genomics. It allows users to input clinical or variant-related free text, and it returns predicted ACMG (American College of Medical Genetics and Genomics) classification attributes such as **PVS1**, **PM2**, **BS1**, etc., with reasoning — all powered by Large Language Models (LLMs) and semantic search.

---

## ✨ Features

- 🔍 Google-like search interface for clinicians, researchers, and analysts
- 🧠 Uses LLMs to classify text into **ACMG variant attributes**
- 📂 PDF upload and semantic chunking with HuggingFace embeddings
- ⚡ Fast, accurate search using FAISS vector store
- ✅ Supports both Pathogenic and Benign ACMG criteria

---

## ⚙️ Tech Stack

- 🧠 LLMs (Gemini, GPT, or custom)
- 🤗 HuggingFace Transformers (`all-MiniLM-L6-v2`)
- 🧬 LangChain for parsing, chunking, retrieval
- 📚 FAISS for dense vector similarity
- 📄 PyMuPDF or pdfminer for PDF loading

---

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/Rishi8860/GeneSearch.git
cd GeneSearch
```
### Install Python Dependencies
```bash
pip install -r requirements.txt
```
### Run the app (FastAPI example)
```bash
uvicorn app:app --reload
```
## 🤝 Contributing
PRs and issues are welcome! Please raise issues for:
- Feature requests
- Inconsistent classification
- Misinterpreted ACMG rules
