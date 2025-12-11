#!/bin/bash

# Setup script for Smart Content Generator & Research Assistant
# This script helps set up the development environment

echo "=========================================="
echo "Smart Content Generator - Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✅ Virtual environment created"
else
    echo "   ℹ️  Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "   ✅ Dependencies installed"

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data
echo "   ✅ Directories created"

# Check for .env file
echo ""
echo "🔑 Checking environment variables..."
if [ ! -f ".env" ]; then
    echo "   ⚠️  .env file not found"
    echo "   📝 Creating .env from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "   ✅ .env file created"
        echo "   ⚠️  Please edit .env and add your API keys"
    else
        echo "   ⚠️  .env.example not found, creating basic .env..."
        cat > .env << EOF
# Environment Variables for Smart Content Generator
OPENAI_API_KEY=your_openai_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
NEWS_API_KEY=your_news_api_key_here
LOG_LEVEL=INFO
LOG_DIR=logs
EOF
        echo "   ✅ Basic .env file created"
        echo "   ⚠️  Please edit .env and add your API keys"
    fi
else
    echo "   ✅ .env file exists"
fi

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the application: streamlit run app.py"
echo ""
echo "For more information, see README.md"
echo ""
