# Digital Foreman Infrastructure

This Terraform configuration deploys the complete serverless infrastructure for the Digital Foreman MVP on Google Cloud Platform using ElevenLabs Conversational AI.

## Architecture Overview

```
Telegram Bot → Cloud Function → ElevenLabs Agent → Firestore → Airtable Dashboard
                    ↓
              Emergency Alerts (Gmail)
                    ↓
              Follow-up Scheduler
```

## Quick Deploy (10 minutes)

### 1. Prerequisites (5 minutes)
- Google Cloud SDK installed and configured
- Terraform >= 1.5 installed  
- Active Google Cloud Project with billing enabled

### 2. External Services Setup (3 minutes)
```bash
# Create ElevenLabs conversational agent
./scripts/setup_agent.sh

# Set up other services (see docs/TECHNICAL_SPEC.md External Services Setup)
```

### 3. Deploy Infrastructure (2 minutes)
```bash
# Deploy everything
./deploy.sh your-project-id
```

## What Gets Deployed

### Serverless Functions
- **telegram-voice-handler**: Processes voice messages via ElevenLabs agent
- **airtable-sync**: Real-time incident data sync to Airtable  
- **followup-scheduler**: Daily automated follow-up messages

### Data Storage
- **Firestore Database**: Incident records and conversation history
- **Cloud Storage**: Audio conversation logs (7-day lifecycle)
- **Secret Manager**: Secure API key storage

### Automation
- **Cloud Scheduler**: Daily follow-up job
- **Eventarc**: Firestore → Airtable sync triggers

### Google APIs Enabled
- Cloud Functions API
- Firestore API
- Cloud Storage API
- Secret Manager API
- Gmail API
- Cloud Scheduler API
- Eventarc API

## Cost Optimization

**Serverless Architecture Benefits:**
- Pay-per-use Cloud Functions (no idle costs)
- Auto-scaling based on demand
- 7-day audio file cleanup
- Minimal always-on resources

**Development (24 hours):**
- Cloud Functions: ~$1
- Firestore: ~$1
- ElevenLabs: ~$3 (conversation usage)
- Storage: <$1
- **Total: <$5**

## Performance Characteristics

- **Voice Response Time**: <2 seconds (ElevenLabs native processing)
- **Concurrent Conversations**: 50+ (Cloud Functions auto-scaling)
- **Uptime**: 99.9% (Google Cloud SLA)
- **Dashboard Updates**: Real-time via Eventarc triggers

## External Service Integration

### ElevenLabs Conversational AI
- **Agent Model**: eleven_flash_v2_5 (low latency)
- **Voice**: Rachel (professional, clear)
- **Features**: Native voice-to-voice conversations
- **Capacity**: Unlimited concurrent conversations

### Telegram Bot
- **Webhook**: Cloud Function HTTPS endpoint
- **File Types**: Voice messages (.ogg format)
- **Response**: Voice replies via ElevenLabs agent

### Airtable Dashboard
- **Sync**: Real-time via Cloud Function triggers
- **Views**: Emergency, Urgent, Open incidents
- **Mobile**: Native app support

## Security Features

- **Serverless Isolation**: Each function runs in isolated container
- **Secret Manager**: All API keys encrypted at rest
- **IAM**: Minimal permissions per service account
- **HTTPS**: All external communications encrypted
- **Auto-cleanup**: Audio files deleted after 7 days

## Monitoring & Debugging

### Cloud Functions Logs
```bash
# View function logs
gcloud functions logs read telegram-voice-handler --region=us-central1

# Real-time monitoring
gcloud functions logs tail telegram-voice-handler --region=us-central1
```

### Key Metrics to Monitor
- Function execution duration (target: <5s)
- Error rates (target: <1%)
- ElevenLabs API latency
- Firestore write operations
- Airtable sync success rate

## Development Workflow

### Local Testing
```bash
# Test functions locally
cd functions/
functions-framework --target=telegram_handler --debug
```

### Deployment Updates
```bash
# Update function code only
cd infrastructure/
terraform apply -target=google_cloudfunctions2_function.telegram_handler
```

### Configuration Changes
```bash
# Update secrets
gcloud secrets versions add telegram-bot-token --data-file=new_token.txt

# Update Terraform variables
edit terraform.tfvars
terraform apply
```

## Troubleshooting

### Common Issues

1. **"Function deployment failed"**
   - Check Cloud Build API is enabled
   - Verify function source code syntax
   - Review Cloud Build logs

2. **"ElevenLabs agent not responding"**
   - Verify agent ID is correct in terraform.tfvars
   - Check ElevenLabs credits/quota
   - Test agent directly in ElevenLabs dashboard

3. **"Firestore permission denied"**
   - Check service account has firestore.user role
   - Verify Firestore database exists in project

4. **"Airtable sync not working"**
   - Verify Airtable base ID format (starts with 'app')
   - Check Airtable API key permissions
   - Review airtable-sync function logs

### Debug Commands
```bash
# Check function status
gcloud functions describe telegram-voice-handler --region=us-central1

# View secret values (for debugging)
gcloud secrets versions access latest --secret=elevenlabs-api-key

# Test webhook manually
curl -X POST https://your-function-url \
  -H "Content-Type: application/json" \
  -d '{"test": "payload"}'
```

## Cleanup

```bash
# Remove all resources
cd infrastructure/
terraform destroy

# Cleanup local files
rm -f terraform.tfstate* .terraform.lock.hcl
rm -rf .terraform/
```

## Template Reusability

This infrastructure creates reusable components for future hackathons:

### Core Template
- Serverless voice processing pipeline
- ElevenLabs conversational AI integration
- Real-time dashboard sync
- Automated follow-up system

### Customization Points
- Change AI agent prompts for different domains
- Swap Airtable for other dashboard providers
- Modify follow-up schedules
- Add additional notification channels

### One-Command Setup
```bash
git clone <template-repo>
./scripts/setup_agent.sh
./deploy.sh new-project-id
```

Perfect for 12-hour hackathon implementations!