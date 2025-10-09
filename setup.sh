#!/bin/bash

# Rosetta CLI Setup Script
# This script helps you set up the environment for Rosetta CLI

echo "🚀 Rosetta CLI Setup"
echo "===================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ".env file created!"
    echo ""
    echo "IMPORTANT: Edit the .env file and add your OpenAI API key"
    echo "   1. Open .env in your text editor"
    echo "   2. Replace 'your-openai-api-key-here' with your actual API key"
    echo "   3. Get your API key from: https://platform.openai.com/account/api-keys"
    echo ""
else
    echo "✅ .env file already exists"
fi

# Check if dependencies are installed
echo "Checking dependencies..."
if python3 -c "import openai, pandas, openpyxl" 2>/dev/null; then
    echo "✅ All dependencies are installed"
else
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    echo "✅ Dependencies installed!"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Quick Start:"
echo "   # Basic scan (no API key needed)"
echo "   python3 main.py /path/to/project"
echo ""
echo "   # With AI translation (requires API key)"
echo "   python3 main.py /path/to/project --excel --translate"
echo ""
echo "   # Test with sample file"
echo "   python3 main.py ./tests/clean-test.vue --log"