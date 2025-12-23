# Development Checklist
## Digital Foreman MVP - No-Code Implementation

### Pre-Development Setup (30 minutes)
- [ ] Telegram bot token obtained from @BotFather (5 min)
- [ ] Terraform infrastructure template deployed (15 min)
- [ ] n8n instance accessible and configured (5 min) 
- [ ] Airtable base created from template (3 min)
- [ ] Twilio account credentials configured (2 min)

### Sprint 1 Checklist: Core Workflow Development

#### Voice Processing Pipeline (4 hours)
- [ ] n8n Telegram webhook trigger configured
- [ ] Voice file download node working
- [ ] Audio format conversion via external API
- [ ] Vertex AI Speech-to-Text HTTP node working
- [ ] Basic voice → text flow tested and working

#### AI Classification & Routing (4 hours)
- [ ] Vertex AI Gemini HTTP node configured
- [ ] Incident classification prompt template loaded
- [ ] Classification JSON parsing working
- [ ] Firestore write node saving incidents correctly
- [ ] Urgency-based routing (If/Switch nodes) working
- [ ] Emergency SMS trigger via Twilio node functional
- [ ] Telegram confirmation message sending

### Sprint 2 Checklist: Intelligence & Dashboard

#### Smart Triage Enhancement (4 hours)
- [ ] Construction terminology added to AI prompt template
- [ ] Location extraction logic improved in prompt
- [ ] Confidence threshold tuning via n8n If nodes (>0.8)
- [ ] Test incident data created for validation
- [ ] Classification accuracy >90% verified on test data

#### Dashboard & Follow-up Automation (4 hours)  
- [ ] Airtable base configured with incident views
- [ ] n8n → Airtable sync workflow operational
- [ ] Real-time data updates flowing to Airtable
- [ ] Scheduled follow-up workflow (24h trigger) working
- [ ] Follow-up message templates configured in n8n
- [ ] Status filtering and urgency views in Airtable

### Sprint 3 Checklist: Testing & Demo Preparation (6 hours)

#### End-to-End Testing & Performance (4 hours)
- [ ] Complete voice → dashboard workflow tested
- [ ] Error scenarios tested (network failures, invalid audio)
- [ ] n8n workflow performance optimized
- [ ] Demo environment tested and stable
- [ ] Backup demo data seeded in Airtable

#### Demo Readiness (2 hours)
- [ ] Demo script written and rehearsed
- [ ] Test incidents prepared for live demo
- [ ] Fallback plan documented for technical issues
- [ ] QR codes generated for bot access
- [ ] Airtable views optimized for demo presentation

### No-Code Quality Standards
- [ ] All n8n workflows have error handling nodes
- [ ] Workflow execution logging enabled
- [ ] Credentials stored in n8n credential store (not hardcoded)
- [ ] Environment variables used via n8n settings
- [ ] Workflow documentation added for handoff

### Security Checklist
- [ ] All API credentials secured in Secret Manager
- [ ] n8n credential store configured properly
- [ ] Firestore security rules configured
- [ ] No PII visible in n8n execution logs
- [ ] Rate limiting configured on n8n webhooks

### Infrastructure Checklist (Terraform-managed)
- [ ] All GCP resources deployed via Terraform
- [ ] n8n instance running on Cloud Run
- [ ] Database backups enabled for n8n PostgreSQL
- [ ] Firestore security rules applied
- [ ] Cloud Run monitoring/alerting configured

### Final Demo Checklist
- [ ] Telegram bot responding to voice messages
- [ ] Emergency SMS alerts triggering correctly
- [ ] Airtable dashboard showing real-time incident data
- [ ] n8n workflows executing under 5 seconds
- [ ] Mobile access working on demo device
- [ ] Backup plan ready if live demo fails

### Reusable Template Creation
- [ ] Terraform modules documented and tagged
- [ ] n8n workflow templates exported and saved
- [ ] Airtable base template created
- [ ] One-command deployment script tested
- [ ] README created for template usage

### Post-Demo Activities
- [ ] Demo data cleared from production systems
- [ ] Cloud costs reviewed and optimized
- [ ] Feedback documented for template improvements
- [ ] Template repository organized for future hackathons