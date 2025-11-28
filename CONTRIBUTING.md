# Contributing to Multi-RAG ChatPDF

Thank you for your interest in contributing to Multi-RAG ChatPDF! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

We welcome suggestions! Please create an issue with:
- A clear, descriptive title
- Detailed description of the proposed feature
- Why this enhancement would be useful
- Possible implementation approach (optional)

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/multi_rag_chatpdf.git
   cd multi_rag_chatpdf
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow the code style guidelines below
   - Add tests if applicable
   - Update documentation as needed

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add amazing feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your feature branch
   - Describe your changes in detail

## 📝 Code Style Guidelines

### Python

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

Example:
```python
def process_pdf(file_path: str) -> list[str]:
    """
    Process a PDF file and extract text chunks.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        List of text chunks
    """
    # Implementation here
    pass
```

### Streamlit

- Keep UI code separate from business logic
- Use session state appropriately
- Add helpful error messages
- Ensure responsive design

### Comments

- Write self-documenting code
- Add comments for complex logic
- Keep comments up-to-date with code changes

## 🧪 Testing

Before submitting a PR:

1. **Test locally**
   ```bash
   streamlit run app.py
   ```

2. **Test with Docker**
   ```bash
   docker build -t multi-rag-chatpdf .
   docker run -p 8501:8501 -e OPENAI_API_KEY=your_key multi-rag-chatpdf
   ```

3. **Check for common issues**
   - No hardcoded API keys
   - No sensitive data in commits
   - All dependencies in requirements.txt
   - Code works with different PDF types

## 📚 Documentation

- Update README.md if adding new features
- Update DEPLOYMENT.md for deployment changes
- Add inline comments for complex code
- Update docstrings

## 🎯 Development Setup

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/multi_rag_chatpdf.git
   cd multi_rag_chatpdf
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

3. **Run in development mode**
   ```bash
   streamlit run app.py
   ```

## 🔍 Code Review Process

All submissions require review. We'll look for:

- Code quality and style
- Test coverage
- Documentation
- Performance implications
- Security considerations

## 📋 Commit Message Guidelines

Use clear, descriptive commit messages:

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

Examples:
```
feat: Add support for password-protected PDFs
fix: Resolve memory leak in PDF processing
docs: Update deployment guide for AWS
```

## 🌟 Areas for Contribution

We especially welcome contributions in:

- **Features**
  - Support for more document types (Word, Excel, etc.)
  - Advanced search capabilities
  - Multi-language support
  - Export conversation history

- **Performance**
  - Caching improvements
  - Faster PDF processing
  - Optimized embeddings

- **UI/UX**
  - Better mobile experience
  - Dark mode
  - Accessibility improvements

- **Documentation**
  - More examples
  - Video tutorials
  - Translation to other languages

- **Testing**
  - Unit tests
  - Integration tests
  - Performance benchmarks

## ❓ Questions?

Feel free to:
- Open an issue for discussion
- Join our community discussions
- Reach out to maintainers

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Multi-RAG ChatPDF! 🎉
