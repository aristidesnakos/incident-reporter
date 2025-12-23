# Technical Specification
## Digital Foreman MVP - No-Code Architecture

### Architecture Overview
```
Telegram Bot → n8n Webhook → n8n Workflows → Vertex AI → Firestore → Airtable Dashboard
```

### Technology Stack
- **Workflow Engine**: n8n (self-hosted on Cloud Run)
- **Bot Platform**: Telegram Bot API (via n8n Telegram nodes)
- **AI**: Vertex AI Gemini 1.5 Flash (via n8n HTTP nodes)
- **Database**: Firestore (via n8n Google Firestore nodes)
- **Storage**: Cloud Storage (via n8n Google Cloud Storage nodes)
- **Dashboard**: Airtable (via n8n Airtable nodes)
- **Notifications**: Twilio SMS (via n8n Twilio nodes)
- **Infrastructure**: Terraform for repeatable deployments

### Data Models

#### Incident Document (Firestore)
```json
{
  "id": "auto-generated",
  "timestamp": "2024-01-15T10:30:00Z",
  "user_id": "telegram_user_id",
  "user_name": "John Smith", 
  "raw_transcript": "There's a wet floor in zone 3",
  "audio_file_url": "gs://bucket/audio123.ogg",
  "classification": {
    "urgency": "emergency|urgent|routine",
    "type": "injury|near-miss|hazard|equipment", 
    "location": "Zone 3",
    "confidence": 0.85
  },
  "status": "open|resolved",
  "follow_ups": [
    {
      "timestamp": "2024-01-16T10:30:00Z",
      "message": "Was this resolved?",
      "response": "Yes, cleaned up"
    }
  ]
}
```

### n8n Workflow Specifications

#### 1. Main Voice Processing Workflow
```
Trigger: Telegram Webhook
↓
Download Voice File (Telegram node)
↓
Convert Audio Format (HTTP node to external service)
↓
Speech-to-Text (HTTP node to Vertex AI)
↓
Classify Incident (HTTP node to Vertex AI Gemini)
↓
Store in Firestore (Google Firestore node)
↓
Route by Urgency (If/Switch node)
├── Emergency → Send SMS (Twilio node)
├── Urgent → Send Telegram Alert  
└── Routine → Log only
↓
Send Confirmation (Telegram node)
```

#### 2. Follow-up Automation Workflow
```
Trigger: Schedule (every 24 hours)
↓
Query Unresolved Incidents (Google Firestore node)
↓
For Each Open Incident (Loop node)
├── Check Time Since Reported
├── Send Follow-up Message (Telegram node)
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

### AI Classification Prompt Template
```
Classify this construction safety incident: {{$json.transcript}}

Return JSON only:
{
  "urgency": "emergency|urgent|routine",
  "type": "injury|near-miss|hazard|equipment",  
  "location": "extracted location or 'unknown'",
  "confidence": 0.0-1.0
}

Classification Rules:
- Emergency = injury occurred or immediate danger
- Urgent = could cause injury within hours
- Routine = general safety concern

Construction Terms:
- Fall protection, scaffolding, heavy machinery
- PPE violations, electrical hazards
- Material handling, excavation safety
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
- Twilio account for SMS alerts
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
- Voice processing: <5 seconds (n8n workflow execution)
- Dashboard load time: <1 second (Airtable native performance)
- Support 10 concurrent workflows
- 99% uptime via Cloud Run auto-scaling

### Monitoring
- n8n workflow execution metrics via built-in monitoring
- Cloud Run metrics (CPU, memory, request latency)
- Vertex AI API usage and latency
- Airtable sync success rate