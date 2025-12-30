#!/bin/bash

# Digital Foreman - One-Command Infrastructure Deployment Script
# Usage: ./deploy.sh [project-id]

set -e

echo "🚀 Digital Foreman Infrastructure Deployment"
echo "============================================="

# Check prerequisites
command -v terraform >/dev/null 2>&1 || { echo "❌ Terraform is required but not installed. Aborting." >&2; exit 1; }
command -v gcloud >/dev/null 2>&1 || command -v ~/google-cloud-sdk/bin/gcloud >/dev/null 2>&1 || { echo "❌ Google Cloud SDK is required but not installed. Aborting." >&2; exit 1; }

# Get project ID
if [ -z "$1" ]; then
    echo "📝 Enter your Google Cloud Project ID:"
    read -r PROJECT_ID
else
    PROJECT_ID="$1"
fi

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Project ID is required. Aborting."
    exit 1
fi

echo ""
echo "🔧 Before we deploy, please ensure you have:"
echo "1. ✅ Created Telegram bot token (@BotFather)"
echo "2. ✅ Created ElevenLabs agent (./scripts/setup_agent.sh)"
echo "3. ✅ Created Airtable base"
echo ""
echo "If you haven't completed these steps, press Ctrl+C to exit and run setup first."
echo "Otherwise, press Enter to continue..."
read -r

# Set up authentication
echo "🔐 Setting up Google Cloud authentication..."
# Use gcloud from PATH or fallback to full path
GCLOUD_CMD=$(command -v gcloud || echo ~/google-cloud-sdk/bin/gcloud)
$GCLOUD_CMD auth application-default login --quiet || true
$GCLOUD_CMD config set project "$PROJECT_ID"

# Navigate to infrastructure directory
cd infrastructure

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    echo "📝 Creating terraform.tfvars from template..."
    cp terraform.tfvars.example terraform.tfvars
    
    echo ""
    echo "❗ Please edit terraform.tfvars with your actual values:"
    echo "   - project_id: $PROJECT_ID (already set)"
    echo "   - telegram_bot_token: from @BotFather"
    echo "   - elevenlabs_api_key: from elevenlabs.io" 
    echo "   - elevenlabs_agent_id: from ./scripts/setup_agent.sh"
    echo "   - airtable_pat: from airtable.com"
    echo "   - airtable_base_id: from your Airtable base URL"
    echo ""
    echo "Run this script again after editing terraform.tfvars"
    exit 0
fi

# Set project_id in terraform.tfvars if not already set correctly
if ! grep -q "project_id.*=.*\"$PROJECT_ID\"" terraform.tfvars; then
    sed -i.bak "s/project_id = \".*\"/project_id = \"$PROJECT_ID\"/" terraform.tfvars
    echo "✅ Updated project_id in terraform.tfvars"
fi

echo "🔧 Initializing Terraform..."
terraform init

echo "📋 Planning deployment..."
terraform plan -var="project_id=$PROJECT_ID"

echo ""
echo "🚀 Ready to deploy infrastructure. This will:"
echo "   - Create Cloud Functions for voice processing"
echo "   - Set up Firestore database"
echo "   - Configure Cloud Storage for audio files"
echo "   - Deploy Cloud Scheduler for follow-ups"
echo "   - Store all secrets in Secret Manager"
echo ""
echo "Continue? (y/N):"
read -r CONFIRM

if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

echo "🚀 Deploying infrastructure..."
terraform apply -auto-approve -var="project_id=$PROJECT_ID"

echo ""
echo "✅ Infrastructure deployment complete!"
echo ""

# Get outputs
WEBHOOK_URL=$(terraform output -raw telegram_webhook_url 2>/dev/null || echo "Not available")
AUDIO_BUCKET=$(terraform output -raw audio_bucket_name 2>/dev/null || echo "Not available")

echo "📊 Deployment Summary:"
echo "🔗 Telegram Webhook URL: $WEBHOOK_URL"
echo "📦 Audio Storage Bucket: $AUDIO_BUCKET"
echo "🆔 Project ID: $PROJECT_ID"

echo ""
echo "📋 Next Steps:"
echo "1. 🤖 Set Telegram webhook:"
echo "   curl -F \"url=$WEBHOOK_URL\" https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook"
echo ""
echo "2. 🧪 Test your bot:"
echo "   - Send voice message to your Telegram bot"
echo "   - Check Cloud Functions logs in Google Console"
echo "   - Verify data appears in Airtable"
echo ""
echo "3. 📊 Monitor the system:"
echo "   - Cloud Functions: https://console.cloud.google.com/functions"
echo "   - Firestore: https://console.cloud.google.com/firestore"
echo "   - Logs: https://console.cloud.google.com/logs"

echo ""
echo "💰 Estimated cost for 24h development: <$5"
echo "🧹 To cleanup: terraform destroy"

echo ""
echo "🎉 Digital Foreman is ready for voice-powered safety reporting!"