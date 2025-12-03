#!/bin/bash
# Setup script for OpenAI Assistant Implementation

set -e  # Exit on error

echo "=========================================="
echo "OpenAI Assistant Setup"
echo "=========================================="
echo ""

# Check if .venv exists
if [ -d ".venv" ]; then
    VENV_PATH=".venv"
elif [ -d "venv" ]; then
    VENV_PATH="venv"
else
    echo "❌ Virtual environment not found!"
    echo "   Creating .venv..."
    python3 -m venv .venv
    VENV_PATH=".venv"
fi

# Activate virtual environment
echo "✅ Activating virtual environment: $VENV_PATH"
source "$VENV_PATH/bin/activate"

# Install/upgrade dependencies
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install openai python-dotenv

# Check for .env file
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo ""
    echo "⚠️  .env file not found at: $ENV_FILE"
    echo "   Please create .env file with:"
    echo "   OPENAI_API_KEY=your_api_key_here"
else
    echo ""
    echo "✅ .env file found at: $ENV_FILE"
fi

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "To run the script:"
echo "  source $VENV_PATH/bin/activate"
echo "  python implement_assistant.py"
echo ""

