#!/bin/bash
# Quick setup script for GitHub Repo Reader

echo "🚀 GitHub Repo Reader - Quick Setup"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed"
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip3 install -r requirements.txt
else
    echo "⚠️  requirements.txt not found, installing basic dependencies..."
    pip3 install flask requests python-dotenv
fi

# Run configuration setup
echo "🔧 Setting up configuration..."
python3 setup_config.py

echo ""
echo "✅ Setup complete!"
echo "🎯 Next: Add your API tokens to .env file"
echo "🚀 Then run: python3 app.py"
