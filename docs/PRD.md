# Product Requirements Document (PRD)
## Digital Foreman MVP - Conversational AI Voice Safety Reporter

### Product Vision
Native voice-to-voice conversational AI safety companion that eliminates reporting friction through natural speech interactions via Telegram bot. Uses ElevenLabs Conversational AI Agent API + Google Cloud Functions to create human-like voice interactions for incident reporting, while creating reusable templates for future hackathons.

### Success Metrics
- **Primary**: Incident reporting time: 5 minutes → 30 seconds via natural conversation
- **Secondary**: Worker participation rate: 20% → 80% through improved UX
- **Technical**: 95% voice transcription accuracy, <3 second conversational response time
- **Conversational**: Natural voice interactions feel human-like (ElevenLabs + Gemini)
- **Development**: 24-hour implementation vs 72-hour traditional development

### Target User
Construction workers on active job sites who need to report safety incidents quickly without removing gloves or navigating complex forms.

### Core User Stories

#### Epic 1: Conversational Voice Incident Capture
```
As a construction worker
I want to have natural voice conversations with an AI safety companion
So that I can quickly report incidents through natural speech without forms or typing

Acceptance Criteria:
- QR code leads to conversational Telegram bot
- Bot accepts voice messages and responds with natural voice
- Bot asks follow-up questions conversationally via ElevenLabs voice
- Vertex AI Gemini understands construction safety context
- Voice transcription accuracy >90% for safety terminology
- Complete conversation flow under 60 seconds
```

#### Epic 2: Conversational Intelligence & Triage
```
As a site safety manager
I want incidents automatically categorized through natural AI conversation
So that I can respond to critical issues immediately with proper context

Acceptance Criteria:
- AI extracts incident details through conversational prompts
- EMERGENCY: Auto-email alert within 30 seconds
- URGENT: Telegram alert within 5 minutes  
- ROUTINE: Added to daily dashboard
- 90% accurate urgency classification via Gemini conversation
- Natural follow-up questions improve data quality
```

#### Epic 3: Auto-Follow-Up
```
As a safety compliance officer
I want unresolved incidents automatically tracked
So that nothing falls through the cracks

Acceptance Criteria:
- Follow-up message sent 24h after initial report
- Incident status updated based on response
- Escalation if no response after 48h
```

#### Epic 4: Real-Time Dashboard
```
As a project manager
I want a real-time view of safety incidents via Airtable
So that I can track resolution status without custom development

Acceptance Criteria:
- Live incident data synced from Cloud Functions
- Pre-built Airtable views for urgency filtering
- Native mobile access via Airtable app
- Real-time updates without refresh
- Built-in CSV export from Airtable
```

### Technical Innovation Goals
- **Native Voice Conversations**: ElevenLabs Conversational AI Agent handles voice-to-voice natively
- **Serverless Architecture**: Google Cloud Functions + ElevenLabs Agent (no complex orchestration)
- **Infrastructure as Code**: Terraform templates for one-command deployment
- **Reusable Templates**: Create hackathon starter kit for voice/conversational AI projects
- **Natural Voice UX**: Human-like personality using ElevenLabs conversational agent
- **Rapid MVP**: Demonstrate 80% faster development time vs traditional approach

### Out of Scope (V1)
- Custom React dashboard (replaced with Airtable)
- Complex workflow orchestration (replaced with ElevenLabs agent + Cloud Functions)
- Integration with Procore/ACC APIs
- Smart helmet hardware
- Photo attachments
- Multilingual support
- Advanced analytics beyond Airtable's native features
- User management system beyond Telegram authentication

### Definition of Done
- End-to-end voice-to-voice reporting works through ElevenLabs Conversational Agent
- Natural voice conversations feel human-like using native ElevenLabs capabilities
- Emergency incidents trigger email alerts within 30 seconds
- Airtable dashboard shows real-time incident data with conversation transcripts
- System handles 10 concurrent voice conversations
- Demo-ready with seeded test data and sample voice conversations
- **Bonus**: Reusable ElevenLabs + Cloud Functions template documented for future hackathons