# Product Requirements Document (PRD)
## Digital Foreman MVP - No-Code Voice Safety Reporter

### Product Vision
Voice-activated safety companion built entirely with no-code tools that eliminates reporting friction through Telegram bot interface and AI-powered incident triage, while creating reusable templates for future hackathons.

### Success Metrics
- **Primary**: Incident reporting time: 5 minutes → 30 seconds
- **Secondary**: Worker participation rate: 20% → 80%
- **Technical**: 95% voice transcription accuracy, <3 second response time
- **Development**: 24-hour implementation vs 72-hour traditional development

### Target User
Construction workers on active job sites who need to report safety incidents quickly without removing gloves or navigating complex forms.

### Core User Stories

#### Epic 1: Voice Incident Capture
```
As a construction worker
I want to report safety incidents by voice message to Telegram
So that I can quickly log incidents without typing on small screens with gloves

Acceptance Criteria:
- QR code leads to Telegram bot
- Bot accepts voice messages up to 5MB
- Bot responds with confirmation within 5 seconds
- Voice transcription accuracy >90% for basic safety terms
```

#### Epic 2: Intelligent Triage
```
As a site safety manager
I want incidents automatically categorized by urgency
So that I can respond to critical issues immediately

Acceptance Criteria:
- EMERGENCY: Auto-SMS within 30 seconds
- URGENT: Telegram alert within 5 minutes  
- ROUTINE: Added to daily dashboard
- 90% accurate urgency classification
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
- **No-Code First**: Zero custom application code - only n8n workflows and configurations
- **Infrastructure as Code**: Terraform templates for one-command deployment
- **Reusable Templates**: Create hackathon starter kit for voice/AI projects
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
- End-to-end voice reporting works through n8n workflows
- Emergency incidents trigger SMS via Twilio node within 30 seconds
- Airtable dashboard shows real-time incident data
- System handles 10 concurrent n8n workflow executions
- Demo-ready with seeded test data in Airtable
- **Bonus**: Reusable template documented and ready for future hackathons