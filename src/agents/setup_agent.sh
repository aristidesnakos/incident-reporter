#!/bin/bash

# Digital Foreman - ElevenLabs Agent Setup Script
# This script helps create the conversational AI agent for safety incident reporting

set -e

echo "🚀 Digital Foreman - ElevenLabs Agent Setup"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    echo "Please install pip3 and try again."
    exit 1
fi

echo "✅ Python 3 and pip3 found"

# Navigate to scripts directory
cd "$(dirname "$0")"

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    echo "ELEVENLABS_API_KEY=your_api_key_here" > .env
    echo ""
    echo "❗ Please edit the .env file with your ElevenLabs API key:"
    echo "   1. Go to https://elevenlabs.io/app/settings/api-keys"
    echo "   2. Create a new API key"
    echo "   3. Edit .env file: ELEVENLABS_API_KEY=sk_your_actual_key"
    echo "   4. Run this script again"
    exit 0
fi

# Check if API key is set
API_KEY=$(grep "ELEVENLABS_API_KEY" .env | cut -d '=' -f2)
if [ "$API_KEY" = "your_api_key_here" ] || [ -z "$API_KEY" ]; then
    echo "❗ Please set your actual ElevenLabs API key in .env file"
    echo "   Current value: $API_KEY"
    exit 1
fi

echo "✅ ElevenLabs API key found"

# Create the agent
echo "🤖 Creating ElevenLabs conversational agent..."
python3 create_agent.py

echo ""
echo "✅ Agent setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Copy the Agent ID from above to your terraform.tfvars file"
echo "2. Test the agent at: https://elevenlabs.io/app/conversational-ai" 
echo "3. Deploy infrastructure: cd ../infrastructure && ./deploy.sh"

# Deactivate virtual environment
deactivate