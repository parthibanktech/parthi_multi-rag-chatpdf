# 🤖 Multi-RAG ChatPDF

A powerful AI-powered PDF chat application that allows you to have intelligent conversations with your PDF documents using RAG (Retrieval-Augmented Generation) technology.

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.40.1-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 📄 **Multi-PDF Support**: Upload and process multiple PDF documents simultaneously
- 🔍 **Intelligent Search**: Uses FAISS vector database for fast and accurate semantic search
- 💬 **Natural Conversations**: Powered by OpenAI's GPT-4o-mini for human-like responses
- 🎯 **Context-Aware**: Retrieves relevant information from your documents to answer questions
- 🚀 **Fast Processing**: Efficient chunking and embedding strategies
- 🎨 **Modern UI**: Clean and intuitive Streamlit interface with auto-scrolling chat

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-4o-mini
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector Database**: FAISS
- **PDF Processing**: pypdf
- **Language**: Python 3.11

## 📋 Prerequisites

- Python 3.9 - 3.12
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

## 🚀 Quick Start

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/multi_rag_chatpdf.git
   cd multi_rag_chatpdf
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Or create `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   
   Navigate to `http://localhost:8501`

### 🐳 Docker Installation

1. **Build the Docker image**
   ```bash
   docker build -t multi-rag-chatpdf .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 \
     -e OPENAI_API_KEY=your_openai_api_key_here \
     multi-rag-chatpdf
   ```

3. **Access the application**
   
   Open `http://localhost:8501` in your browser

### 🌐 Deploy to Streamlit Cloud

1. **Fork this repository** to your GitHub account

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Create a new app**:
   - Select your forked repository
   - Set the main file path: `app.py`
   - Click "Advanced settings"

4. **Add secrets**:
   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```

5. **Deploy!** 🎉

## 📖 Usage

1. **Upload PDFs**: Click on the sidebar and upload one or more PDF files
2. **Process**: Click the "Process" button to analyze your documents
3. **Ask Questions**: Type your questions in the input box
4. **Get Answers**: The AI will respond based on the content of your PDFs

## 🏗️ Project Structure

```
multi_rag_chatpdf/
├── app.py                 # Main application file
├── htmlTemplates.py       # HTML templates for UI components
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker ignore patterns
├── .gitignore           # Git ignore patterns
├── README.md            # This file
├── .streamlit/
│   └── secrets.toml     # Streamlit secrets (not in git)
└── .env                 # Environment variables (not in git)
```

## ⚙️ Configuration

You can customize the following parameters in `app.py`:

```python
EMBED_MODEL = "text-embedding-3-small"  # OpenAI embedding model
CHAT_MODEL = "gpt-4o-mini"              # OpenAI chat model
CHUNK_SIZE = 1000                        # Text chunk size
TOP_K = 5                                # Number of relevant chunks to retrieve
```

## 🔒 Security

- Never commit your `.env` file or `secrets.toml` to version control
- Keep your OpenAI API key secure
- Use environment variables for sensitive data
- The `.gitignore` file is configured to exclude sensitive files

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for their powerful language models
- Streamlit for the amazing web framework
- FAISS for efficient vector search
- The open-source community

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ using Streamlit and OpenAI**
