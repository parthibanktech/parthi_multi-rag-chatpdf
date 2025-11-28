# 🚀 Deployment Guide

This guide covers all deployment options for the Multi-RAG ChatPDF application.

## Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Streamlit Cloud](#streamlit-cloud-deployment)
- [GitHub Setup](#github-setup)
- [Production Considerations](#production-considerations)

---

## 🖥️ Local Development

### Prerequisites
- Python 3.9 - 3.12
- OpenAI API Key

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/multi_rag_chatpdf.git
   cd multi_rag_chatpdf
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the app**
   
   Open your browser at `http://localhost:8501`

---

## 🐳 Docker Deployment

### Option 1: Docker Run

1. **Build the image**
   ```bash
   docker build -t multi-rag-chatpdf .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 \
     -e OPENAI_API_KEY=sk-your-actual-key-here \
     multi-rag-chatpdf
   ```

3. **Access the app**
   
   Open `http://localhost:8501`

### Option 2: Docker Compose

1. **Create `.env` file**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your API key.

2. **Start the application**
   ```bash
   docker-compose up -d
   ```

3. **View logs**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the application**
   ```bash
   docker-compose down
   ```

### Option 3: Pull from GitHub Container Registry

Once you've pushed to GitHub:

```bash
docker pull ghcr.io/yourusername/multi_rag_chatpdf:latest

docker run -p 8501:8501 \
  -e OPENAI_API_KEY=sk-your-actual-key-here \
  ghcr.io/yourusername/multi_rag_chatpdf:latest
```

---

## ☁️ Streamlit Cloud Deployment

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [streamlit.io/cloud](https://streamlit.io/cloud))
- OpenAI API Key

### Steps

1. **Push code to GitHub** (see [GitHub Setup](#github-setup) below)

2. **Go to Streamlit Cloud**
   
   Visit [share.streamlit.io](https://share.streamlit.io)

3. **Create new app**
   - Click "New app"
   - Select your repository: `yourusername/multi_rag_chatpdf`
   - Branch: `main` or `master`
   - Main file path: `app.py`

4. **Configure secrets**
   
   Click "Advanced settings" → "Secrets"
   
   Add your OpenAI API key:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-key-here"
   ```

5. **Deploy**
   
   Click "Deploy!" and wait for the build to complete.

6. **Access your app**
   
   Your app will be available at: `https://yourusername-multi-rag-chatpdf-app-xxxxx.streamlit.app`

### Updating Your Deployment

Simply push changes to your GitHub repository:
```bash
git add .
git commit -m "Update application"
git push origin main
```

Streamlit Cloud will automatically rebuild and redeploy.

---

## 🔧 GitHub Setup

### Initial Setup

1. **Initialize Git** (if not already done)
   ```bash
   git init
   ```

2. **Add all files**
   ```bash
   git add .
   ```

3. **Create initial commit**
   ```bash
   git commit -m "Initial commit: Multi-RAG ChatPDF application"
   ```

4. **Create GitHub repository**
   
   Go to [github.com/new](https://github.com/new) and create a new repository named `multi_rag_chatpdf`

5. **Add remote and push**
   ```bash
   git remote add origin https://github.com/yourusername/multi_rag_chatpdf.git
   git branch -M main
   git push -u origin main
   ```

### Enable GitHub Container Registry

The GitHub Actions workflow will automatically build and push Docker images to GitHub Container Registry (GHCR).

1. **Enable GitHub Actions**
   
   Go to your repository → Settings → Actions → General
   
   Enable "Read and write permissions" for workflows

2. **Make package public** (optional)
   
   After first push, go to your repository → Packages
   
   Click on your package → Package settings → Change visibility → Public

### Continuous Deployment

Every push to `main` will:
- Run tests
- Build Docker image
- Push to GitHub Container Registry
- Tag with commit SHA and branch name

---

## 🔒 Production Considerations

### Security

1. **API Key Management**
   - Never commit `.env` or `secrets.toml` files
   - Use environment variables or secrets management
   - Rotate API keys regularly

2. **Rate Limiting**
   - Monitor OpenAI API usage
   - Implement rate limiting if needed
   - Set up usage alerts

3. **HTTPS**
   - Streamlit Cloud provides HTTPS automatically
   - For custom deployments, use reverse proxy (nginx) with SSL

### Performance

1. **Caching**
   - Consider implementing caching for embeddings
   - Use `@st.cache_data` for expensive operations

2. **Scaling**
   - For high traffic, consider:
     - Multiple container instances
     - Load balancer
     - Redis for session state

3. **Monitoring**
   - Set up application monitoring
   - Track API costs
   - Monitor error rates

### Cost Optimization

1. **OpenAI API**
   - Use `gpt-4o-mini` for cost-effective responses
   - Implement token limits
   - Cache embeddings when possible

2. **Infrastructure**
   - Streamlit Cloud: Free tier available
   - Docker: Use multi-stage builds (already implemented)
   - Consider serverless options for low traffic

---

## 📊 Monitoring and Logs

### Docker Logs

```bash
# View logs
docker logs multi-rag-chatpdf

# Follow logs
docker logs -f multi-rag-chatpdf

# Docker Compose
docker-compose logs -f
```

### Streamlit Cloud Logs

Access logs from your Streamlit Cloud dashboard:
- Go to your app
- Click "Manage app"
- View logs in real-time

---

## 🆘 Troubleshooting

### Common Issues

1. **"Missing OPENAI_API_KEY" error**
   - Ensure API key is set in `.env` or Streamlit secrets
   - Check for typos in environment variable name

2. **Docker build fails**
   - Check Docker is running
   - Ensure you have enough disk space
   - Try `docker system prune` to clean up

3. **Streamlit Cloud deployment fails**
   - Check `requirements.txt` is valid
   - Ensure all files are committed to GitHub
   - Check Streamlit Cloud logs for specific errors

4. **PDF processing errors**
   - Ensure PDFs are not password-protected
   - Check PDF file size limits
   - Verify PDF is not corrupted

### Getting Help

- Open an issue on GitHub
- Check Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
- OpenAI API docs: [platform.openai.com/docs](https://platform.openai.com/docs)

---

## 🎉 Next Steps

After deployment:

1. **Test thoroughly** with various PDF documents
2. **Monitor costs** in OpenAI dashboard
3. **Gather user feedback**
4. **Iterate and improve**

---

**Happy Deploying! 🚀**
