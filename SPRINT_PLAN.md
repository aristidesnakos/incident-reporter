# Sprint Planning & Roadmap
## Digital Foreman MVP - 24 Hour No-Code Development Plan

### Sprint 0: Infrastructure Setup (2 hours)
**Goal**: Complete infrastructure deployment using reusable templates

**Tasks:**
- [ ] Create Telegram bot via @BotFather (15 min)
- [ ] Deploy Terraform infrastructure template (45 min)
  - GCP project with required APIs
  - Firestore database + Cloud Storage
  - Service accounts with proper IAM
- [ ] Deploy n8n instance on Cloud Run (30 min)
- [ ] Set up Airtable base from template (15 min)
- [ ] Configure Twilio SMS credentials (15 min)

**Definition of Done**: All infrastructure deployed, n8n accessible, Airtable ready

---

### Sprint 1: Core Workflow Development (8 hours)

#### Hour 1-4: Primary Voice Processing Pipeline
**Assignee**: Workflow Engineer

**Tasks:**
- [ ] Telegram webhook → n8n workflow setup (1h)
- [ ] Voice file download and conversion nodes (1h)
- [ ] Vertex AI Speech-to-Text integration (1h)
- [ ] Test voice message → transcript flow (1h)

**Definition of Done**: Voice messages converted to text in n8n

#### Hour 5-8: AI Classification & Routing
**Assignee**: AI Engineer

**Tasks:**
- [ ] Vertex AI Gemini node for incident classification (2h)
- [ ] Incident urgency routing logic (1h)
- [ ] Firestore write operations from n8n (1h)
- [ ] Emergency SMS trigger via Twilio node (2h)
- [ ] Basic error handling in workflow (2h)

**Definition of Done**: Voice → Classification → Database + Emergency SMS working

---

### Sprint 2: Intelligence & Dashboard (8 hours)

#### Hour 9-12: Smart Triage Enhancement
**Assignee**: AI Engineer

**Tasks:**
- [ ] Improve AI prompts for construction terminology (2h)
- [ ] Location extraction enhancement (1h)
- [ ] Confidence threshold tuning (1h)

**Definition of Done**: >90% accurate classification on test data

#### Hour 13-16: Dashboard & Follow-up Automation
**Assignee**: Dashboard Engineer

**Tasks:**
- [ ] n8n → Airtable sync workflow (1h)
- [ ] Airtable views for urgency filtering (1h)
- [ ] Scheduled follow-up workflow in n8n (2h)

**Definition of Done**: Real-time dashboard showing incidents, automated follow-ups

---

### Sprint 3: Testing & Demo Preparation (6 hours)

#### Hour 17-22: End-to-End Testing & Polish
**Assignee**: All Team

**Tasks:**
- [ ] End-to-end workflow testing (2h)
- [ ] Performance optimization in n8n (1h)
- [ ] Demo data preparation (1h)
- [ ] Demo script rehearsal (1h)
- [ ] Backup plan testing (1h)

**Definition of Done**: Successful demo run with contingencies tested

### Progress Checkpoints
- **Hour 2**: Infrastructure fully deployed
- **Hour 8**: Voice → AI → Database pipeline working
- **Hour 16**: Dashboard live with real-time data
- **Hour 22**: Demo ready with backup plan

### Scope Protection Rules
1. **No custom code** - use n8n nodes and pre-built services only
2. **Template-first approach** - leverage existing workflow templates
3. **Demo over perfection** - working demo beats complex features
4. **Ask PM before** any architecture changes

### Reusable Hackathon Template
This project creates reusable components for future hackathons:

**Infrastructure Template** (`/infrastructure`):
- Terraform modules for GCP + Firestore setup
- n8n deployment on Cloud Run
- Service account configurations

**Workflow Templates** (`/workflows`):
- Voice processing pipeline (Telegram → AI → Database)
- SMS alerting with Twilio
- Automated follow-up scheduling
- Database sync to external dashboards

**Dashboard Templates** (`/dashboards`):
- Airtable base with incident tracking views
- Real-time sync configuration
- Mobile-responsive layouts

**Deployment**: One-command infrastructure setup with `terraform apply`