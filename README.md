# 🧠 PaperMind - AI Research Paper Discovery Engine

PaperMind is an AI-powered Research Paper Discovery Engine that enables users to search, process, and interact with research papers using Retrieval-Augmented Generation (RAG). The application combines semantic search, vector embeddings, and Large Language Models (LLMs) to provide intelligent answers based on research papers.

> 🚧 **Project Status:** Under Active Development  
> New features, optimizations, and improvements will be added regularly.

---

# 🚀 Features

- 🔍 Search research papers using the arXiv API
- 📄 View detailed paper information
- 📥 Download and process research papers
- 🧹 Automatic PDF text extraction and cleaning
- ✂️ Semantic text chunking
- 🧠 Generate embeddings using Sentence Transformers
- ⚡ Store embeddings in FAISS Vector Database
- 🤖 AI-powered Question Answering using Groq LLM
- 💬 Interactive AI Assistant
- 📚 Retrieval-Augmented Generation (RAG)
- 🗂 Conversation History
- 🎨 Modern Responsive UI
- 🏗 Modular Flask Architecture

---

# 🛠 Tech Stack

## Backend

- Python
- Flask
- Flask-SQLAlchemy

## AI & Machine Learning

- Groq API
- Sentence Transformers
- FAISS
- Transformers
- PyTorch

## Data Processing

- PyMuPDF
- PyPDF2
- NumPy
- Pandas
- Scikit-Learn

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

---

# ⚙ Project Workflow

```
Search Paper
      │
      ▼
Fetch from arXiv API
      │
      ▼
Download PDF
      │
      ▼
Extract Text
      │
      ▼
Clean Text
      │
      ▼
Create Semantic Chunks
      │
      ▼
Generate Embeddings
      │
      ▼
Store in FAISS
      │
      ▼
Ask Questions
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Generate Answer using Groq
```

---

# 📂 Project Structure

```
AI_Research_Paper_Discovery_Engine/

├── api/
├── data/
├── embeddings/
├── llm/
├── models/
├── pdf_processing/
├── providers/
├── repositories/
├── services/
├── static/
├── templates/
├── utils/
├── vectorstore/

├── app.py
├── config.py
├── requirements.txt
└── README.md
```

---

# ⚡ Installation

Clone the repository

```bash
git clone https://github.com/your-username/AI_Research_Paper_Discovery_Engine.git
```

Move into the project

```bash
cd AI_Research_Paper_Discovery_Engine
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Create `.env`

```env
SECRET_KEY=your_secret_key
GROQ_API_KEY=your_api_key
DATABASE_URI=sqlite:///papers.db
DEBUG=True
```

Run the application

```bash
python app.py
```

---

# 💻 Usage

1. Search a research paper
2. Open paper details
3. Process the paper
4. Open AI Assistant
5. Ask questions related to the paper
6. Receive AI-generated responses

---

# 🎯 Current Modules

- Research Paper Search
- Paper Details
- PDF Processing
- Text Cleaning
- Semantic Chunking
- Embedding Generation
- Vector Database
- AI Assistant
- Retrieval-Augmented Generation (RAG)

---

# 🚀 Future Improvements

- Multi-Paper Chat
- Citation Network Visualization
- Research Paper Comparison
- AI Research Recommendations
- Hybrid Search (BM25 + FAISS)
- Cross-Encoder Re-ranking
- User Authentication
- Cloud Deployment
- Export Chat to PDF
- Research History Dashboard

---

# 🤝 Contributing

Contributions, suggestions, and feature requests are welcome.

Feel free to fork the repository and submit a Pull Request.

---

# 📄 License

This project is intended for educational and research purposes.

---

# 👨‍💻 Author

**Adarsh Mundhe**

AI & Machine Learning Enthusiast

---

## ⭐ Project Status

> This project is actively being improved.
>
> New features, performance optimizations, UI enhancements, and AI capabilities will continue to be added in future updates.

If you find this project useful, consider giving it a ⭐ on GitHub.
