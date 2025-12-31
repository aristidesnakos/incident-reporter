# Technical Specification
## Digital Foreman MVP - Web-Based Conversational AI Architecture

### Architecture Overview
```
Web Page → ElevenLabs Conversational AI Widget → [Optional: Webhook] → Airtable Dashboard
```

### Technology Stack
- **Voice AI**: ElevenLabs Conversational AI Widget (native voice-to-voice)
- **Frontend**: Single HTML page (no framework required)
- **Backend**: Optional webhook endpoint (for data capture)
- **Dashboard**: Airtable (real-time incident tracking)
- **Deployment**: Static file hosting or local file
- **Infrastructure**: Zero infrastructure required

### Data Models

#### Incident Record (Airtable)
```json
{
  "Incident_ID": "INC-001", 
  "Timestamp": "2024-01-15T10:30:00Z",
  "Reporter": "John Smith",
  "Conversation_Summary": "Wet floor hazard in Zone 3, approximately 10 square feet near entrance, no warning signs posted",
  "Urgency": "Emergency|Urgent|Routine",
  "Type": "Injury|Near-Miss|Hazard|Equipment",
  "Location": "Zone 3", 
  "Status": "Open|In Progress|Resolved",
  "AI_Confidence": "85%",
  "Conversation_Link": "https://elevenlabs.ai/conversation/abc123" 
}
```

### Implementation Details

#### 1. Web Interface (`index.html`)
```html
<!DOCTYPE html>
<html>
<head>
    <title>Digital Foreman - Voice Safety Reporter</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Mobile-first responsive design */
        body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
        .hero { text-align: center; margin-bottom: 40px; }
        .widget-container { display: flex; justify-content: center; margin: 40px 0; }
    </style>
</head>
<body>
    <div class="hero">
        <h1>Digital Foreman</h1>
        <p>Voice-Powered Safety Incident Reporting</p>
        <p>Click below to start a voice conversation with our AI safety assistant</p>
    </div>
    
    <div class="widget-container">
        <elevenlabs-convai agent-id="agent_8401kdqtgnnbfx18q1fv460mh7pv"></elevenlabs-convai>
    </div>

    <script src="https://unpkg.com/@elevenlabs/convai-widget-embed@beta" async type="text/javascript"></script>
</body>
</html>
```

#### 2. Optional Data Capture (webhook endpoint)
```javascript
// Optional: ElevenLabs webhook to capture conversation data
app.post('/webhook/elevenlabs', (req, res) => {
    const conversationData = req.body;
    
    // Extract incident details from conversation
    const incident = {
        timestamp: new Date().toISOString(),
        summary: conversationData.transcript,
        urgency: conversationData.metadata.urgency,
        location: conversationData.metadata.location
    };
    
    // Send to Airtable via API
    airtable.create(incident);
    
    res.status(200).send('OK');
});
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

#### Telegram Bot (3 minutes) DONE
1. Message @BotFather in Telegram
2. Send `/newbot` → name: "SaifetyBot"  
3. Username: "SaifetyBot"
4. Copy bot token for terraform.tfvars
5. Configure: `/setdescription` - Voice-activated safety incident reporting

#### ElevenLabs Conversational AI Agent (5 minutes)
1. Sign up at elevenlabs.io (free tier: 10,000 chars/month)
2. Profile → API Keys → Create "Digital Foreman Bot" 
3. Run `./src/agents/setup_agent.sh` to create agent
4. Copy Agent ID and API key for terraform.tfvars
5. Test at elevenlabs.io/app/conversational-ai

#### Airtable Dashboard (5 minutes)  DONE
1. Create base: "Digital Foreman Incidents"
2. Configure fields: ID, Timestamp, User Name, Incident Type (Injury/Near-miss/Hazard/Equipment), Urgency (Emergency/Urgent/Routine), Location, Description, Status, Follow-up Count, Confidence Score
3. Create views: Emergency, Open Incidents, Today's Reports, Location Summary
4. Get API key and Base ID from airtable.com/api

#### terraform.tfvars Configuration DONE
```hcl
project_id = "your-gcp-project-id"
telegram_bot_token = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  
elevenlabs_api_key = "sk_1234567890abcdefghijklmnopqrstuvwxyz"
elevenlabs_agent_id = "agent_1234567890abcdefghijklmnop"
airtable_pat = "patABCDEFGHIJKLMNOPQRSTUVWXYZ.1234567890abcdef"
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