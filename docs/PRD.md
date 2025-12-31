# Product Requirements Document (PRD)
## Digital Foreman MVP - Web-Based Conversational AI Voice Safety Reporter

### Product Vision
Native voice-to-voice conversational AI safety companion accessible via simple web interface. Uses ElevenLabs Conversational AI Widget to create human-like voice interactions for incident reporting with zero infrastructure complexity, while creating reusable templates for future hackathons.

### Success Metrics
- **Primary**: Incident reporting time: 5 minutes → 30 seconds via natural conversation
- **Secondary**: Worker participation rate: 20% → 80% through improved UX
- **Technical**: 95% voice conversation accuracy, <2 second response time 
- **Conversational**: Natural voice interactions feel human-like (ElevenLabs Conversational AI)
- **Development**: 12-hour implementation vs 24-hour traditional development

### Target User
Construction workers on active job sites who need to report safety incidents quickly without removing gloves or navigating complex forms.

### Core User Stories

#### Epic 1: Conversational Voice Incident Capture
```
As a construction worker
I want to have natural voice conversations with an AI safety companion
So that I can quickly report incidents through natural speech without forms or typing

Acceptance Criteria:
- Workers access web page with embedded ElevenLabs voice widget
- Widget enables native voice-to-voice conversations (no typing)
- AI asks follow-up questions conversationally using ElevenLabs agent
- ElevenLabs Conversational AI understands construction safety context
- Voice conversation accuracy >90% for safety terminology  
- Complete conversation flow under 60 seconds
- Works on mobile browsers (no app installation required)
```

#### Epic 2: Conversational Intelligence & Triage
```
As a site safety manager
I want incidents automatically categorized through natural AI conversation
So that I can respond to critical issues immediately with proper context

Acceptance Criteria:
- AI extracts incident details through conversational prompts
- EMERGENCY: Real-time dashboard alert with audio notification
- URGENT: Dashboard highlight within 5 minutes  
- ROUTINE: Added to daily dashboard
- 90% accurate urgency classification via ElevenLabs Conversational AI
- Natural follow-up questions improve data quality
- Incidents appear in Airtable dashboard immediately
```

#### Epic 3: Auto-Follow-Up
```
As a safety compliance officer
I want unresolved incidents automatically tracked
So that nothing falls through the cracks

Acceptance Criteria:
- Dashboard shows incidents requiring follow-up (24h+ unresolved)
- Email notifications for overdue incidents
- Manual follow-up conversations via same web interface
- Incident status updated based on dashboard actions
- Escalation workflows built into Airtable
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
- **Native Voice Conversations**: ElevenLabs Conversational AI Widget handles voice-to-voice natively
- **Zero Infrastructure**: Single HTML page + ElevenLabs widget (no servers, no deployment complexity)
- **Instant Setup**: Copy/paste widget code - working voice AI in 60 seconds
- **Reusable Templates**: Create hackathon starter kit for voice/conversational AI projects
- **Natural Voice UX**: Human-like personality using ElevenLabs conversational agent
- **Rapid MVP**: Demonstrate 90% faster development time vs traditional approach

### Out of Scope (V1)
- Custom React dashboard (replaced with Airtable)
- Complex backend infrastructure (replaced with ElevenLabs widget)
- Integration with Procore/ACC APIs
- Smart helmet hardware
- Photo attachments
- Multilingual support
- Advanced analytics beyond Airtable's native features
- User authentication system (open access web page)

### Definition of Done
- End-to-end voice-to-voice reporting works through ElevenLabs Widget in web page
- Natural voice conversations feel human-like using native ElevenLabs capabilities
- Emergency incidents show immediate alerts in Airtable dashboard
- Airtable dashboard shows real-time incident data with conversation transcripts
- Web page works on mobile and desktop browsers
- Demo-ready with seeded test data and sample voice conversations
- **Bonus**: Reusable ElevenLabs widget template documented for future hackathons