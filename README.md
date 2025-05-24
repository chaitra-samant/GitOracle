# 🔍 GitOracle


A powerful Retrieval-Augmented Generation (RAG) system that helps you understand complex repositories using natural language. Built with FastAPI backend and Streamlit frontend.

## 🌟 Features

- **Repository Ingestion**: Clone and process any public GitHub repository
- **Intelligent Chunking**: Automatically splits code files into meaningful chunks
- **Vector Search**: Uses embeddings to find relevant code snippets
- **Natural Language Queries**: Ask questions about repositories in plain English 
- **Interactive UI**: Clean Streamlit interface for easy interaction
- **Real-time Processing**: Live feedback during repository ingestion

## 📁 Project Structure

```
├── Backend 
│   ├── ingest.py (Extracts Contents from Repository)
│   ├── rag.py (RAG Implementation)
│   ├── main.py (FastAPI Backend)
│   └── processed_files.json (Stores Files for faster lookup)
│
└── app.py (Streamlit UI)
```

## 🚀 Quick Start



### 1. Clone the Repository

```bash
git clone <https://github.com/chaitra-samant/GitOracle>
cd GitOracle
```

### 2. Install Dependencies

```bash
python -m env myenv
myenv/Scripts/activate
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the root directory:

```env
#GROQ API 
GROQ_API_KEY=your_groq_api_key_here

# API Configuration
API_BASE_URL=deployed_url_here

```

### 4. Run the Application

#### Start FastAPI Backend
```bash
# Terminal 1
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Start Streamlit Frontend
```bash
# Terminal 2
streamlit run streamlit_app.py --server.port 8501
```

### 5. Access the Application

- **Streamlit UI**: http://localhost:8501
- **FastAPI Docs**: http://localhost:8000/docs

## 📋 Using Application

### Ingesting a Repository

1. Open the Streamlit interface
2. Enter a GitHub repository URL (e.g., `https://github.com/username/repo`)
3. Click "🚀 Ingest Repository"
4. Wait for processing to complete

### Querying the Repository

1. After ingestion, use the "Query Repository" section
2. Ask questions like:
   - "What does this repository do?"
   - "How do I use the main function?"
   - "What are the key components?"
   - "Show me the database models"



## 🔧 Configuration

### Supported File Types

The system processes these file types by default:
- `.py` (Python)
- `.js`, `.jsx` (JavaScript)
- `.ts`, `.tsx` (TypeScript)
- `.java` (Java)
- `.cpp`, `.c`, `.h` (C/C++)
- `.cs` (C#)
- `.go` (Go)
- `.rs` (Rust)
- `.md` (Markdown)
- `.txt` (Text)
- `.yml`, `.yaml` (YAML)
- `.json` (JSON)


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

