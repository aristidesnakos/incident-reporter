# Product Requirements Document (PRD)
## Digital Foreman MVP - No-Code Voice Safety Reporter

### Product Vision
Conversational AI safety companion built entirely with no-code tools that eliminates reporting friction through natural voice conversations via Telegram bot. Uses ElevenLabs + Google Cloud Vertex AI to create human-like interactions for incident reporting, while creating reusable templates for future hackathons.

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

#### Epic 4: No-Code Dashboard
```
As a project manager
I want a real-time view of safety incidents via Airtable
So that I can track resolution status without custom development

Acceptance Criteria:
- Live incident data synced from n8n workflows
- Pre-built Airtable views for urgency filtering
- Native mobile access via Airtable app
- Real-time updates without refresh
- Built-in CSV export from Airtable
```

### Technical Innovation Goals
- **Conversational AI Integration**: ElevenLabs + Google Cloud Vertex AI via n8n HTTP nodes
- **No-Code First**: Zero custom application code - only visual n8n workflows
- **Infrastructure as Code**: Terraform templates for one-command deployment
- **Reusable Templates**: Create hackathon starter kit for voice/conversational AI projects
- **Natural Voice UX**: Human-like personality and voice using ElevenLabs synthesis
- **Rapid MVP**: Demonstrate 67% faster development time vs traditional approach

### Out of Scope (V1)
- Custom React dashboard (replaced with Airtable)
- Complex backend APIs (replaced with n8n workflows)  
- Integration with Procore/ACC APIs
- Smart helmet hardware
- Photo attachments
- Multilingual support
- Advanced analytics beyond Airtable's native features
- User management system beyond Telegram authentication

### Definition of Done
- End-to-end conversational voice reporting works through n8n workflows
- Natural voice conversations via ElevenLabs + Gemini feel human-like
- Emergency incidents trigger email alerts within 30 seconds
- Airtable dashboard shows real-time incident data with conversation transcripts
- System handles 10 concurrent conversational workflow executions
- Demo-ready with seeded test data and sample voice conversations
- **Bonus**: Reusable conversational AI template documented for future hackathons