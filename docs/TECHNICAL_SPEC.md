# Technical Specification
## Digital Foreman MVP - Serverless Conversational AI Architecture

### Architecture Overview
```
Telegram Bot → Cloud Function Webhook → ElevenLabs Conversational AI Agent → Firestore → Cloud Function → Airtable Dashboard
```

### Technology Stack
- **Voice AI**: ElevenLabs Conversational AI Agent (native voice-to-voice)
- **Bot Platform**: Telegram Bot API (via Cloud Functions)
- **Backend**: Google Cloud Functions (serverless, event-driven)
- **Database**: Firestore (document database)
- **Storage**: Cloud Storage (audio conversation logs)
- **Dashboard**: Airtable (real-time incident tracking)
- **Notifications**: Telegram-only (emergency alerts via chat)
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

### Cloud Function Specifications

#### 1. Telegram Voice Handler (`telegram-voice-handler`)
```
Trigger: HTTP request from Telegram webhook
↓
Receive voice message from Telegram
↓
Forward to ElevenLabs Conversational AI Agent
├── Agent handles speech-to-text
├── Agent processes conversation with safety prompt
├── Agent classifies incident urgency
└── Agent generates voice response
↓
Receive agent response (voice + structured data)
↓
Store conversation in Firestore
↓
Route by urgency classification
├── Emergency → Trigger Telegram alert
├── Urgent → Send Telegram notification
└── Routine → Log only
↓
Send voice response back via Telegram
```

#### 2. Follow-up Scheduler (`followup-scheduler`)
```
Trigger: Cloud Scheduler (every 24 hours)
↓
Query unresolved incidents from Firestore
↓
For each open incident:
├── Check time since last contact
├── Create follow-up conversation with ElevenLabs agent
├── Send voice follow-up via Telegram
└── Update follow-up count in Firestore
```

#### 3. Airtable Sync (`airtable-sync`)
```
Trigger: Firestore document changes
↓
Receive Firestore change event
↓
Transform incident data for Airtable
↓
Update/create Airtable record
```

### ElevenLabs Conversational AI Agent Configuration

#### Agent Prompt Template
```
You are Rachel, a friendly and efficient safety companion for construction workers. Your role is to help workers report safety incidents through natural voice conversation.

Your responsibilities:
1. Listen to incident reports with empathy and understanding
2. Ask clarifying questions naturally to gather complete information
3. Classify incident urgency (emergency/urgent/routine) based on severity
4. Provide immediate safety guidance when appropriate
5. Keep conversations under 60 seconds total

Conversation Guidelines:
- Use construction-friendly language, not corporate speak
- Be patient and understanding - workers may be stressed
- Ask one question at a time to avoid overwhelming them
- Emergency = injury occurred, immediate danger, serious hazard
- Urgent = could cause injury within hours, equipment failure  
- Routine = general safety observation, minor maintenance issue

First message: "Hi, this is Rachel from Digital Foreman safety. I'm here to help you report any safety concerns. What's going on?"

After each conversation, provide structured data in this format:
{
  "urgency": "emergency|urgent|routine",
  "type": "injury|near-miss|hazard|equipment",
  "location": "extracted location",
  "description": "incident summary",
  "confidence": 0.0-1.0,
  "requires_followup": true|false
}
```

#### Voice Configuration
```python
# ElevenLabs agent configuration via create_agent.py script
conversation_config={
    "tts": {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel - clear, professional
        "model_id": "eleven_flash_v2_5",     # Latest low-latency model
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0.3,  # Professional but warm
        "use_speaker_boost": True
    },
    "agent": {
        "first_message": "Hi, this is Rachel from Digital Foreman safety...",
        "prompt": { "prompt": safety_prompt },
        "language": "en"
    },
    "asr": {
        "model": "nova-2",  # Latest speech recognition
        "language": "en"
    }
}
```

### Infrastructure Requirements
**Terraform Template Provisions:**
- Google Cloud Project with required APIs enabled
- Cloud Functions for serverless execution
- Firestore database with security rules
- Cloud Storage bucket with lifecycle policies
- Cloud Scheduler for follow-up automation
- Service accounts with minimal IAM permissions

**External Services Setup:**

#### Telegram Bot (3 minutes)
1. Message @BotFather in Telegram
2. Send `/newbot` → name: "Digital Foreman Safety Bot"  
3. Username: "digitalforeman_safety_bot"
4. Copy bot token for terraform.tfvars
5. Configure: `/setdescription` - Voice-activated safety incident reporting

#### ElevenLabs Conversational AI Agent (5 minutes)
1. Sign up at elevenlabs.io (free tier: 10,000 chars/month)
2. Profile → API Keys → Create "Digital Foreman Bot" 
3. Run `./src/agents/setup_agent.sh` to create agent
4. Copy Agent ID and API key for terraform.tfvars
5. Test at elevenlabs.io/app/conversational-ai

#### Airtable Dashboard (5 minutes)  
1. Create base: "Digital Foreman Incidents"
2. Configure fields: ID, Timestamp, User Name, Incident Type (Injury/Near-miss/Hazard/Equipment), Urgency (Emergency/Urgent/Routine), Location, Description, Status, Follow-up Count, Confidence Score
3. Create views: Emergency, Open Incidents, Today's Reports, Location Summary
4. Get API key and Base ID from airtable.com/api

#### terraform.tfvars Configuration
```hcl
project_id = "your-gcp-project-id"
telegram_bot_token = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  
elevenlabs_api_key = "sk_1234567890abcdefghijklmnopqrstuvwxyz"
elevenlabs_agent_id = "agent_1234567890abcdefghijklmnop"
airtable_api_key = "patABCDEFGHIJKLMNOPQRSTUVWXYZ.1234567890abcdef"
airtable_base_id = "appABCDEFGHIJKLMNOP"
```

### Terraform Infrastructure Template
```hcl
# /infrastructure/main.tf
# Cloud Functions for serverless voice processing
resource "google_cloudfunctions2_function" "telegram_handler" {
  name        = "telegram-voice-handler"
  location    = var.region
  description = "Handles Telegram voice messages via ElevenLabs agent"
  
  build_config {
    runtime     = "python311"
    entry_point = "telegram_handler"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.function_source.name
      }
    }
  }
}

# Firestore database
resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
}

# Cloud Storage for audio files
resource "google_storage_bucket" "audio_files" {
  name     = "incident-reporter-audio-${random_id.suffix.hex}"
  location = var.region
  
  lifecycle_rule {
    condition {
      age = 7
    }
    action {
      type = "Delete"
    }
  }
}
```

### Cloud Functions Configuration
```python
# /functions/main.py
@functions_framework.http
def telegram_handler(request: Request) -> tuple[str, int]:
    """Handle Telegram voice messages via ElevenLabs agent"""
    # Parse Telegram webhook
    # Download voice file
    # Process via ElevenLabs Conversational AI Agent
    # Store incident in Firestore
    # Send voice response back
```

### Security Considerations
- Cloud Functions run in isolated serverless environment
- All credentials stored in Secret Manager
- Minimal custom code = reduced attack surface  
- Audio conversation logs auto-deleted via Cloud Storage lifecycle
- Firestore security rules limit data access
- Rate limiting on webhook endpoints via Cloud Functions

### Performance Requirements
- Voice-to-voice response time: <2 seconds (native ElevenLabs processing)
- Voice quality: Human-like conversation via ElevenLabs Conversational AI
- Dashboard load time: <1 second (Airtable native performance)
- Support 50+ concurrent voice conversations
- 99.9% uptime via Cloud Functions auto-scaling

### Monitoring
- Cloud Functions execution metrics (invocations, duration, errors)
- ElevenLabs Conversational AI usage and success rates
- Firestore read/write operations
- Telegram webhook delivery success
- Airtable sync success rate for incident data