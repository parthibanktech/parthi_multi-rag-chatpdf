# Quick Start Script for Multi-RAG ChatPDF (Windows)
# Run this script in PowerShell

Write-Host "🚀 Multi-RAG ChatPDF - Quick Start" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "📋 Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "✓ $pythonVersion detected" -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host "⚙️  Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  IMPORTANT: Please edit .env and add your OPENAI_API_KEY" -ForegroundColor Red
    Write-Host ""
    $response = Read-Host "Press Enter to open .env file in notepad"
    notepad .env
} else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}
Write-Host ""

# Verify OpenAI API key
$envContent = Get-Content .env -Raw
if ($envContent -match "your_openai_api_key_here") {
    Write-Host "❌ ERROR: Please set your actual OpenAI API key in .env file" -ForegroundColor Red
    Write-Host "   Edit .env and replace 'your_openai_api_key_here' with your actual key" -ForegroundColor Red
    exit 1
}
Write-Host "✓ OpenAI API key configured" -ForegroundColor Green
Write-Host ""

# Run the application
Write-Host "🎉 Setup complete! Starting application..." -ForegroundColor Cyan
Write-Host ""
streamlit run app.py
