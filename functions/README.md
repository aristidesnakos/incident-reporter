# Cloud Functions Templates

This directory contains Cloud Function code for the Digital Foreman MVP. These functions implement the complete serverless voice incident reporting pipeline using ElevenLabs Conversational AI.

## Function Overview

### 1. Telegram Voice Handler (`telegram_handler`)
**Purpose**: Core function for handling voice messages via ElevenLabs agent
**Trigger**: HTTP request from Telegram webhook
**Flow**: Voice → ElevenLabs Agent → Firestore Storage → Response

### 2. Airtable Sync (`airtable_sync`) 
**Purpose**: Real-time sync of incident data to Airtable
**Trigger**: Firestore document changes (Eventarc)
**Flow**: Firestore change → Data transformation → Airtable update

### 3. Follow-up Scheduler (`followup_scheduler`)
**Purpose**: Daily automated follow-up for unresolved incidents
**Trigger**: Cloud Scheduler (daily at 9 AM)
**Flow**: Query open incidents → ElevenLabs agent follow-up → Telegram message

## Quick Setup

1. **Deploy Infrastructure First**:
   ```bash
   ./deploy.sh your-project-id
   ```

2. **Functions Are Auto-Deployed**:
   - Terraform automatically packages and deploys all functions
   - Source code is zipped and uploaded to Cloud Storage
   - Functions are created with proper IAM and environment variables

3. **Configure Telegram Webhook**:
   ```bash
   # Get webhook URL from terraform output
   WEBHOOK_URL=$(terraform output -raw telegram_webhook_url)
   
   # Set webhook
   curl -F "url=$WEBHOOK_URL" \
     https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook
   ```

## Function Details

### Telegram Voice Handler
- **Runtime**: Python 3.11
- **Memory**: 512 MB
- **Timeout**: 60 seconds
- **Concurrency**: Up to 100 instances
- **Environment Variables**:
  - `PROJECT_ID`: Google Cloud project ID
  - `AUDIO_BUCKET`: Cloud Storage bucket for audio files
- **Secrets** (via Secret Manager):
  - `TELEGRAM_BOT_TOKEN`: Bot token from @BotFather
  - `ELEVENLABS_API_KEY`: ElevenLabs API key
  - `ELEVENLABS_AGENT_ID`: Conversational agent ID
  - `GMAIL_CREDENTIALS`: Gmail API credentials (base64)

### Airtable Sync
- **Runtime**: Python 3.11
- **Memory**: 256 MB
- **Timeout**: 30 seconds
- **Trigger**: Firestore document created in `incidents` collection
- **Secrets**:
  - `AIRTABLE_API_KEY`: Airtable API key
  - `AIRTABLE_BASE_ID`: Airtable base ID

### Follow-up Scheduler
- **Runtime**: Python 3.11
- **Memory**: 512 MB
- **Timeout**: 300 seconds (5 minutes)
- **Schedule**: Daily at 9 AM EST
- **Secrets**: Same as Telegram handler (for ElevenLabs and Telegram)

## Dependencies

```txt
functions-framework>=3.5.0
google-cloud-firestore>=2.14.0
google-cloud-storage>=2.12.0
google-cloud-secret-manager>=2.18.1
requests>=2.31.0
flask>=2.3.0
```

## Testing Functions

### Local Testing
```bash
# Test functions locally
cd functions/
functions-framework --target=telegram_handler --debug

# Test with curl
curl -X POST http://localhost:8080 \
  -H "Content-Type: application/json" \
  -d '{"message": {"voice": {"file_id": "test"}}}'
```

### End-to-End Test
1. Send voice message to Telegram bot
2. Check Cloud Functions logs:
   ```bash
   gcloud functions logs read telegram-voice-handler --region=us-central1
   ```
3. Verify incident appears in Firestore
4. Confirm data syncs to Airtable dashboard

### Performance Test
- **Target Response Time**: <2 seconds
- **Voice Quality**: Natural ElevenLabs synthesis
- **Error Rate**: <1%
- **Concurrent Users**: 50+ supported

## Monitoring & Debugging

### Cloud Functions Logs
```bash
# View recent logs
gcloud functions logs read telegram-voice-handler --region=us-central1 --limit=50

# Real-time monitoring
gcloud functions logs tail telegram-voice-handler --region=us-central1

# Filter by severity
gcloud functions logs read telegram-voice-handler --region=us-central1 --filter="severity>=ERROR"
```

### Key Metrics
- Function invocations per minute
- Average execution duration
- Error rate and types
- Memory usage patterns
- Cold start frequency

### Common Debug Scenarios
1. **Voice processing fails**:
   - Check ElevenLabs agent ID is correct
   - Verify API key has sufficient credits
   - Test agent directly in ElevenLabs dashboard

2. **Firestore writes fail**:
   - Check service account has `firestore.user` role
   - Verify Firestore database exists
   - Check for quota limits

3. **Airtable sync fails**:
   - Verify base ID format (starts with 'app')
   - Check API key permissions
   - Ensure field names match exactly

## Function Customization

### Modify ElevenLabs Agent Behavior
1. Update prompt in `scripts/create_agent.py`
2. Recreate agent: `./scripts/setup_agent.sh`
3. Update agent ID in terraform.tfvars
4. Redeploy: `terraform apply`

### Change Voice Response Logic
1. Edit `telegram_handler` function in `main.py`
2. Modify incident classification logic
3. Update urgency routing rules
4. Redeploy functions: `terraform apply`

### Add New External Integrations
1. Add secrets to terraform variables
2. Update function environment variables
3. Modify function code to call new APIs
4. Test integration thoroughly

## Security Features

- **Isolated Execution**: Each function runs in isolated serverless container
- **Secret Management**: All credentials stored in Google Secret Manager
- **IAM**: Minimal permissions per service account
- **HTTPS Only**: All external communications encrypted
- **Auto-cleanup**: Audio files deleted after 7 days
- **Rate Limiting**: Built-in Cloud Functions rate limiting

## Cost Optimization

**Serverless Benefits**:
- Pay-per-request pricing (no idle costs)
- Auto-scaling based on demand
- Minimal memory allocation where possible
- Short timeouts to avoid unnecessary charges

**Estimated Costs** (12h development):
- Function invocations: ~$1
- Compute time: ~$1
- Networking: <$1
- **Total: ~$2**

## Template Reusability

This Cloud Functions template creates reusable components:

### Core Template Features
- Serverless voice processing pipeline
- ElevenLabs conversational AI integration  
- Real-time dashboard sync
- Automated follow-up system

### Customization Points
- Change AI agent prompts for different domains
- Swap Airtable for other dashboard providers
- Modify follow-up schedules
- Add additional notification channels

### One-Command Deployment
```bash
git clone <template-repo>
./scripts/setup_agent.sh
./deploy.sh new-project-id
```

Perfect for rapid hackathon development with proven reliability!