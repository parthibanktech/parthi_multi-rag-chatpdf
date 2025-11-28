#!/bin/bash

# Quick Start Script for Multi-RAG ChatPDF
# This script helps you get started quickly

set -e

echo "🚀 Multi-RAG ChatPDF - Quick Start"
echo "=================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Please edit .env and add your OPENAI_API_KEY"
    echo ""
    read -p "Press Enter to open .env file in default editor..."
    ${EDITOR:-nano} .env
else
    echo "✓ .env file already exists"
fi
echo ""

# Verify OpenAI API key
if grep -q "your_openai_api_key_here" .env; then
    echo "❌ ERROR: Please set your actual OpenAI API key in .env file"
    echo "   Edit .env and replace 'your_openai_api_key_here' with your actual key"
    exit 1
fi
echo "✓ OpenAI API key configured"
echo ""

# Run the application
echo "🎉 Setup complete! Starting application..."
echo ""
streamlit run app.py
