# Sprint Planning & Roadmap
## Digital Foreman MVP - 12 Hour Conversational AI Development Plan

### Sprint 0: Infrastructure Setup (1.5 hours) ⚠️ 95% COMPLETE - BLOCKED BY GCP SERVICE ACCOUNT
**Goal**: Complete serverless infrastructure deployment using reusable templates

**Tasks Completed:**
- [x] Create Telegram bot via @BotFather (10 min)
- [x] Create ElevenLabs Conversational AI Agent (20 min) 
- [x] Set up Airtable base from template (10 min)
- [x] Install and configure Google Cloud SDK
- [x] Switch to `hotspringslist` project with billing enabled
- [x] Deploy 95% of Terraform infrastructure:
  - [x] Firestore database (imported existing)
  - [x] Secret Manager with all API credentials stored
  - [x] Cloud Storage buckets (function source + audio files)
  - [x] Service accounts with proper IAM permissions
  - [x] All required Google Cloud APIs enabled
  - [x] Complete Terraform state with 25+ resources deployed

**Tasks Blocked:**
- [ ] Deploy Cloud Functions (15 min) - **BLOCKED**: Missing default Compute Engine service account `92258738211-compute@developer.gserviceaccount.com`
- [ ] Configure Telegram webhook with deployed Cloud Function URL (5 min) - **BLOCKED**: Cloud Functions not deployed

**Technical Blocker Details:**
- **Root Cause**: Google Cloud project missing default Compute Engine service account
- **Error**: `Service account projects/-/serviceAccounts/92258738211-compute@developer.gserviceaccount.com was not found`
- **Impact**: Cloud Functions cannot be deployed via Terraform
- **Workaround Options**:
  1. Manual Cloud Function deployment via Google Cloud Console
  2. Enable Compute Engine API and create VM to initialize service account
  3. Request Google Cloud support to create default service account

**Status**: Infrastructure foundation 95% complete, final Cloud Functions blocked by GCP service account issue

---

### Sprint 1: Conversational Voice Pipeline (4 hours)

#### Hour 1-2: ElevenLabs Agent Integration
**Assignee**: AI Engineer

**Tasks:**
- [x] Configure ElevenLabs agent with safety prompt (30 min)
- [ ] Test agent voice conversations (30 min) - pending deployment
- [x] Implement Cloud Function webhook handler (30 min)
- [x] Connect Telegram → ElevenLabs agent flow (30 min)

**Definition of Done**: Voice messages trigger ElevenLabs conversations ✅ CODE COMPLETE

#### Hour 3-4: Data Pipeline & Alerts
**Assignee**: Backend Engineer

**Tasks:**
- [x] Extract structured data from agent responses (30 min)
- [x] Implement Firestore storage (30 min)
- [x] Telegram notification routing (emergency/urgent/routine) (30 min)
- [ ] Test end-to-end voice → database flow (30 min) - pending deployment

**Definition of Done**: Voice → ElevenLabs → Database + Telegram Notifications working ✅ CODE COMPLETE

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

### Resume Instructions (Next Session)
1. **FIRST**: Fix GCP service account - create VM to initialize default compute SA
2. Deploy 3 Cloud Functions via Terraform or Console
3. Get webhook URL: `terraform output telegram_webhook_url` 
4. Configure Telegram webhook
5. Test voice pipeline

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