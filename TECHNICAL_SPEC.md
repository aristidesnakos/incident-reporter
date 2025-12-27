# Technical Specification
## Digital Foreman MVP - No-Code Architecture

### Architecture Overview
```
Telegram Bot → n8n Webhook → Speech-to-Text → Gemini Conversation → ElevenLabs Voice → Firestore → Airtable Dashboard
```

### Technology Stack
- **Workflow Engine**: n8n (self-hosted on Cloud Run)
- **Bot Platform**: Telegram Bot API (via n8n Telegram nodes)
- **AI Conversation**: Vertex AI Gemini 1.5 Flash (via n8n HTTP nodes)
- **Voice Synthesis**: ElevenLabs API (via n8n HTTP nodes)
- **Speech Recognition**: Vertex AI Speech-to-Text (via n8n HTTP nodes)
- **Database**: Firestore (via n8n Google Firestore nodes)
- **Storage**: Cloud Storage (via n8n Google Cloud Storage nodes)
- **Dashboard**: Airtable (via n8n Airtable nodes)
- **Notifications**: Gmail API (via n8n Gmail nodes)
- **Infrastructure**: Terraform for repeatable deployments

### Data Models

#### Incident Document (Firestore)
```json
{
  "id": "auto-generated",
  "timestamp": "2024-01-15T10:30:00Z",
  "user_id": "telegram_user_id",
  "user_name": "John Smith", 
  "conversation": {
    "initial_transcript": "There's a wet floor in zone 3",
    "ai_response": "I understand there's a wet floor hazard in zone 3. Can you tell me how large the area is and if there are warning signs up?",
    "user_followup": "It's about 10 square feet near the entrance, no signs yet",
    "ai_classification": "This is an urgent slip hazard that needs immediate attention"
  },
  "audio_files": {
    "user_input": "gs://bucket/user_input_123.ogg",
    "ai_response": "gs://bucket/ai_response_123.mp3"
  },
  "classification": {
    "urgency": "emergency|urgent|routine",
    "type": "injury|near-miss|hazard|equipment", 
    "location": "Zone 3",
    "confidence": 0.85,
    "conversation_quality": 0.92
  },
  "status": "open|resolved",
  "follow_ups": [
    {
      "timestamp": "2024-01-16T10:30:00Z",
      "message": "Was this resolved?",
      "voice_response": "gs://bucket/followup_voice_123.mp3",
      "response": "Yes, cleaned up and signs posted"
    }
  ]
}
```

### n8n Workflow Specifications

#### 1. Conversational Voice Processing Workflow
```
Trigger: Telegram Webhook
↓
Download Voice File (Telegram node)
↓
Convert Audio Format (HTTP node to external service)
↓
Speech-to-Text (HTTP node to Vertex AI)
↓
Conversational AI Processing (HTTP node to Vertex AI Gemini)
├── Initial incident understanding
├── Follow-up questions generation
└── Classification within conversation
↓
Generate Voice Response (HTTP node to ElevenLabs)
↓
Send Voice Response (Telegram node with audio)
↓
Store Conversation in Firestore (Google Firestore node)
↓
Route by Urgency (If/Switch node)
├── Emergency → Send Email Alert (Gmail node)
├── Urgent → Send Telegram Alert  
└── Routine → Log only
↓
Continue Conversation Loop (if needed)
```

#### 2. Conversational Follow-up Automation Workflow
```
Trigger: Schedule (every 24 hours)
↓
Query Unresolved Incidents (Google Firestore node)
↓
For Each Open Incident (Loop node)
├── Check Time Since Reported
├── Generate Personalized Follow-up (Gemini HTTP node)
├── Create Voice Follow-up (ElevenLabs HTTP node)
├── Send Voice Follow-up Message (Telegram node)
└── Update Follow-up Count (Google Firestore node)
```

#### 3. Dashboard Sync Workflow  
```
Trigger: Firestore Changes (Webhook)
↓
Transform Data (Code node)
↓
Update Airtable Record (Airtable node)
```

### AI Conversational Prompt Template
```
You are a helpful safety companion for construction workers. Have a natural conversation to understand the safety incident they're reporting.

User input: {{$json.transcript}}

Your response should:
1. Acknowledge their report with empathy
2. Ask clarifying questions if needed (location, severity, people affected)
3. Provide immediate safety guidance if appropriate
4. Extract incident details naturally through conversation

Then classify the incident:
{
  "urgency": "emergency|urgent|routine",
  "type": "injury|near-miss|hazard|equipment",  
  "location": "extracted location or 'unknown'",
  "confidence": 0.0-1.0,
  "conversation_quality": 0.0-1.0,
  "next_question": "follow-up question if needed",
  "ai_response": "natural conversational response",
  "requires_followup": true|false
}

Conversation Rules:
- Keep responses under 30 seconds when spoken
- Use construction-friendly language (not corporate speak)
- Emergency = injury occurred, immediate danger, or serious hazard
- Urgent = could cause injury within hours, equipment failure
- Routine = general safety observation, minor issue

Be conversational, helpful, and focused on safety.
```

### Infrastructure Requirements
**Terraform Template Provisions:**
- Google Cloud Project with required APIs enabled
- Firestore database with security rules
- Cloud Storage bucket with lifecycle policies
- Cloud Run instance for n8n deployment
- Service accounts with minimal IAM permissions

**External Services:**
- Telegram Bot token from @BotFather
- ElevenLabs API key for voice synthesis
- Gmail API credentials for email alerts
- Airtable workspace and base

### Terraform Infrastructure Template
```hcl
# /infrastructure/main.tf
module "gcp_base" {
  source = "./modules/gcp-base"
  project_id = var.project_id
  region = var.region
}

module "n8n_deployment" {
  source = "./modules/n8n-cloud-run"
  project_id = var.project_id
  region = var.region
}

module "firestore_setup" {
  source = "./modules/firestore"
  project_id = var.project_id
}
```

### n8n Deployment Configuration
```yaml
# n8n on Cloud Run with persistent data
apiVersion: serving.knative.dev/v1
kind: Service
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/cloudsql-instances: n8n-postgres
    spec:
      containers:
      - image: n8nio/n8n:latest
        env:
        - name: N8N_DATABASE_TYPE
          value: postgresdb
```

### Security Considerations
- n8n runs in isolated Cloud Run container
- Credentials stored in Secret Manager
- No custom code = reduced attack surface
- Audio files auto-deleted via Cloud Storage lifecycle
- Firestore security rules limit data access
- Rate limiting on webhook endpoints via n8n

### Performance Requirements
- Conversational response time: <3 seconds (speech-to-text → Gemini → ElevenLabs → response)
- Voice synthesis quality: Clear, natural speech via ElevenLabs
- Dashboard load time: <1 second (Airtable native performance)
- Support 10 concurrent conversational workflows
- 99% uptime via Cloud Run auto-scaling

### Monitoring
- n8n conversational workflow execution metrics via built-in monitoring
- Cloud Run metrics (CPU, memory, request latency)
- Vertex AI API usage and latency (Speech-to-Text + Gemini)
- ElevenLabs API usage and voice generation success rate
- Airtable sync success rate for conversation data