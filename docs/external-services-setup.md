# External Services Setup Guide

This guide walks through configuring all external services needed for the Digital Foreman MVP. Complete these steps before infrastructure deployment.

**Note**: This new architecture uses ElevenLabs Conversational AI Agent instead of separate speech-to-text and text-to-speech services.

## 1. Telegram Bot Setup (3 minutes)

### Create Bot
1. Open Telegram and message **@BotFather**
2. Send `/newbot` command
3. Choose bot name: "Digital Foreman Safety Bot"
4. Choose username: "digitalforeman_safety_bot" (must be unique)
5. **Copy the bot token** - you'll need this for terraform.tfvars

### Configure Bot Settings
```
/setdescription - Voice-activated safety incident reporting for construction sites
/setabouttext - Report safety incidents via voice messages. AI-powered incident classification and emergency alerts.
/setuserpic - Upload a construction safety icon
```

### Test Bot
1. Search for your bot username in Telegram
2. Send `/start` to verify it responds
3. **Save the bot token** for terraform.tfvars configuration

---

## 2. ElevenLabs Conversational AI Agent (5 minutes)

### Create Account
1. Go to [elevenlabs.io](https://elevenlabs.io/)
2. Sign up with email (free tier includes 10,000 characters/month)
3. Verify email address

### Get API Key
1. Go to Profile → API Keys
2. Click "Create API Key"
3. Name: "Digital Foreman Bot"
4. **Copy the API key** - you'll need this for terraform.tfvars

### Create Conversational AI Agent
1. Run the setup script:
   ```bash
   cd scripts/
   ./setup_agent.sh
   ```
2. **Copy the Agent ID** from the script output
3. **Save both API key and Agent ID** for terraform.tfvars
4. Test the agent at [elevenlabs.io/app/conversational-ai](https://elevenlabs.io/app/conversational-ai)

---

## 3. Gmail API Setup (7 minutes)

### Enable Gmail API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (same as infrastructure)
3. APIs & Services → Library
4. Search "Gmail API" → Enable

### Create OAuth2 Credentials
1. APIs & Services → Credentials
2. Click "Create Credentials" → OAuth 2.0 Client ID
3. Application type: Web application
4. Name: "Digital Foreman n8n Gmail"
5. Authorized redirect URIs: `https://accounts.google.com/oauth2/callback` (or leave empty for service account)
6. **Download JSON credentials** - you'll base64 encode this for terraform.tfvars

### Configure OAuth Consent Screen
1. OAuth consent screen → External
2. App name: "Digital Foreman Safety Bot"
3. User support email: your email
4. Scopes: Add Gmail send scope
5. Test users: Add your email

---

## 4. Airtable Dashboard (5 minutes)

### Create Airtable Account
1. Go to [airtable.com](https://airtable.com/)
2. Sign up (free tier sufficient for MVP)
3. Verify email

### Create Base from Template
1. Click "Create a base"
2. Choose "Start from scratch"
3. Name: "Digital Foreman Incidents"

### Configure Tables
**Main Table: "Incidents"**
```
Fields:
- ID (Auto-generated)
- Timestamp (Date/Time) 
- User Name (Single line text)
- Incident Type (Single select: Injury, Near-miss, Hazard, Equipment)
- Urgency (Single select: Emergency, Urgent, Routine)
- Location (Single line text)
- Description (Long text)
- Status (Single select: Open, Resolved)
- Follow-up Count (Number)
- Confidence Score (Number)
```

### Get API Credentials
1. Go to [airtable.com/api](https://airtable.com/api)
2. Select your "Digital Foreman Incidents" base
3. **Copy Base ID** (starts with "app...")
4. Get Personal Access Token from Account → Developer Hub
5. **Save API key and Base ID** for terraform.tfvars

### Create Dashboard Views
1. **Emergency View**: Filter by Urgency = "Emergency"
2. **Open Incidents**: Filter by Status = "Open"  
3. **Today's Reports**: Filter by Timestamp = "Today"
4. **Location Summary**: Group by Location

---

## 5. Terraform Configuration

After gathering all credentials, configure terraform.tfvars:

### Base64 Encode Gmail Credentials
1. Download Gmail OAuth2 JSON file
2. Base64 encode it:
   ```bash
   base64 -w 0 gmail-credentials.json
   ```
3. Copy the output for terraform.tfvars

### Update terraform.tfvars
1. Copy `infrastructure/terraform.tfvars.example` to `infrastructure/terraform.tfvars`
2. Fill in all values:
   ```hcl
   project_id = "your-gcp-project-id"
   telegram_bot_token = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
   elevenlabs_api_key = "sk_1234567890abcdefghijklmnopqrstuvwxyz"
   elevenlabs_agent_id = "agent_1234567890abcdefghijklmnop"
   gmail_credentials_json = "ewogICJ0eXBlIjogIlNlcnZpY2UgQWNjb3VudCIsLi4u"
   airtable_api_key = "patABCDEFGHIJKLMNOPQRSTUVWXYZ.1234567890abcdef"
   airtable_base_id = "appABCDEFGHIJKLMNOP"
   ```

---

## 6. Verification Checklist

### Test Each Service
- [ ] Telegram bot responds to /start command
- [ ] ElevenLabs agent conversation test works
- [ ] Gmail can send test email from configured account
- [ ] Airtable base is accessible and has proper field structure
- [ ] All credentials are configured in terraform.tfvars

### Integration Tests (After Deployment)
- [ ] Send test voice message to Telegram bot
- [ ] Verify ElevenLabs agent responds with voice
- [ ] Check that incident data appears in Airtable dashboard
- [ ] Confirm email alert triggers for emergency incidents

### Performance Validation
- [ ] End-to-end response time < 2 seconds
- [ ] Voice quality is clear and professional
- [ ] No errors in Cloud Functions logs
- [ ] All external API calls succeed

---

## Security Notes

- **Never commit API keys** to version control
- Store all credentials in terraform.tfvars (which is .gitignored)
- Terraform stores credentials in Google Secret Manager automatically
- Use OAuth2 where available (Gmail)
- Regularly rotate API keys
- Monitor usage quotas to avoid unexpected charges

## Cost Monitoring

**Free Tier Limits:**
- ElevenLabs: 10,000 characters/month
- Airtable: 1,200 records/base
- Gmail API: 1 billion quota units/day

**Estimated Costs (12h development):**
- ElevenLabs: $1-3 (conversation usage)
- Cloud Functions: $1-2
- All other services: Free tier sufficient
- **Total: <$5**

## Troubleshooting

### Common Issues
1. **Telegram bot not responding**: Check bot token is correct in terraform.tfvars
2. **ElevenLabs agent fails**: Verify agent ID and API key are correct
3. **Gmail auth errors**: Check base64 encoding of credentials JSON
4. **Airtable sync fails**: Verify base ID format (starts with 'app') and API key
5. **Terraform deployment fails**: Check all required variables are set in terraform.tfvars

### Support Resources
- [Telegram Bot API Docs](https://core.telegram.org/bots/api)
- [ElevenLabs Conversational AI Docs](https://elevenlabs.io/docs/conversational-ai/overview)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Airtable API Docs](https://airtable.com/developers/web/api/introduction)
- [Google Cloud Functions Docs](https://cloud.google.com/functions/docs)