# Sprint Planning & Roadmap
## Digital Foreman MVP - 12 Hour Conversational AI Development Plan

### Sprint 0: Infrastructure Setup (1.5 hours) ✅ COMPLETED
**Goal**: Complete serverless infrastructure deployment using reusable templates

**Tasks Completed:**
- [x] Create Telegram bot via @BotFather (10 min)
- [x] Deploy Terraform infrastructure template (30 min)
  - GCP project with required APIs (Cloud Functions, Firestore)
  - Firestore database + Cloud Storage
  - Service accounts with proper IAM
- [ ] Create ElevenLabs Conversational AI Agent (20 min)
- [ ] Set up Airtable base from template (10 min)
- [ ] Deploy Cloud Functions (15 min)
- [ ] Configure Telegram webhook with deployed Cloud Function URL (5 min)

**Status**: Infrastructure foundation ready, ElevenLabs agent and final integration pending

---

### Sprint 1: Conversational Voice Pipeline (4 hours)

#### Hour 1-2: ElevenLabs Agent Integration
**Assignee**: AI Engineer

**Tasks:**
- [ ] Configure ElevenLabs agent with safety prompt (30 min)
- [ ] Test agent voice conversations (30 min)
- [ ] Implement Cloud Function webhook handler (30 min)
- [ ] Connect Telegram → ElevenLabs agent flow (30 min)

**Definition of Done**: Voice messages trigger ElevenLabs conversations

#### Hour 3-4: Data Pipeline & Alerts
**Assignee**: Backend Engineer

**Tasks:**
- [ ] Extract structured data from agent responses (30 min)
- [ ] Implement Firestore storage (30 min)
- [ ] Telegram notification routing (emergency/urgent/routine) (30 min)
- [ ] Test end-to-end voice → database flow (30 min)

**Definition of Done**: Voice → ElevenLabs → Database + Telegram Notifications working

---

### Sprint 2: Dashboard & Automation (4 hours)

#### Hour 5-6: Real-time Dashboard
**Assignee**: Dashboard Engineer

**Tasks:**
- [ ] Cloud Function → Airtable sync (30 min)
- [ ] Airtable views for urgency filtering (30 min)
- [ ] Test real-time data flow (30 min)
- [ ] Mobile dashboard optimization (30 min)

**Definition of Done**: Real-time incident dashboard operational

#### Hour 7-8: Follow-up Automation
**Assignee**: AI Engineer

**Tasks:**
- [ ] Cloud Scheduler for follow-ups (30 min)
- [ ] ElevenLabs agent follow-up conversations (30 min)
- [ ] Firestore status updates (30 min)
- [ ] Test automated follow-up flow (30 min)

**Definition of Done**: Automated 24h follow-ups via voice

---

### Sprint 3: Testing & Demo Preparation (2.5 hours)

#### Hour 9-11.5: End-to-End Testing & Demo Prep
**Assignee**: All Team

**Tasks:**
- [ ] End-to-end voice conversation testing (45 min)
- [ ] Performance optimization (30 min)
- [ ] Demo data preparation (30 min)
- [ ] Demo script rehearsal (30 min)
- [ ] Backup plan documentation (15 min)

**Definition of Done**: Demo ready with tested backup plan

### Progress Tracking
- **Current Status**: Sprint 0 infrastructure foundation complete
- **Next Milestone**: ElevenLabs agent creation and Cloud Functions deployment
- **Target Completion**: 12 hours total development time

### Progress Checkpoints
- **Hour 1.5**: Infrastructure fully deployed ✅ COMPLETED
- **Hour 4**: Voice → ElevenLabs → Database pipeline working
- **Hour 8**: Dashboard live with automated follow-ups  
- **Hour 11.5**: Demo ready with backup plan

### Current Priorities (Next Session)
1. Complete ElevenLabs Conversational AI Agent setup
2. Deploy Cloud Functions for voice processing
3. Configure Telegram webhook integration
4. Test end-to-end voice → database flow

### Scope Protection Rules
1. **Minimal custom code** - leverage ElevenLabs agent + Cloud Functions only
2. **Template-first approach** - create reusable Cloud Function templates
3. **Demo over perfection** - working voice demo beats complex features
4. **Native voice conversations** - ElevenLabs handles all voice processing

### Reusable Hackathon Template
This project creates reusable components for future hackathons:

**Infrastructure Template** (`/infrastructure`):
- Terraform modules for GCP + Cloud Functions setup
- Firestore and Cloud Storage configuration
- Service account configurations

**Function Templates** (`/src/functions/`):
- Voice conversation handler (Telegram → ElevenLabs Agent → Database)  
- Telegram notification routing (emergency/urgent/routine alerts)
- Automated follow-up scheduling with voice responses
- Database sync to external dashboards

**Dashboard Templates** (`/dashboards`):
- Airtable base with incident tracking views
- Real-time sync configuration
- Mobile-responsive layouts

**Deployment**: One-command infrastructure setup with `terraform apply`