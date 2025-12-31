# Sprint Planning & Roadmap
## Digital Foreman MVP - 4 Hour Web-Based Conversational AI Development Plan

### Sprint 0: Simple Setup (30 minutes) ✅ COMPLETED
**Goal**: Create web-based conversational AI interface with zero infrastructure

**Tasks Completed:**
- [x] Create ElevenLabs Conversational AI Agent (20 min) 
- [x] Set up Airtable base from template (10 min)

**Status**: Core setup complete - ready to build web interface

---

### Sprint 1: Web Interface Development (2 hours)

#### Hour 1: Create Web Interface
**Assignee**: Frontend Developer

**Tasks:**
- [ ] Create HTML page with ElevenLabs widget (30 min)
- [ ] Style interface for mobile/desktop (15 min)
- [ ] Test voice conversations in browser (15 min)

**Definition of Done**: Working web page with voice conversations

#### Hour 2: Data Integration (Optional)
**Assignee**: Backend Engineer

**Tasks:**
- [ ] Set up webhook endpoint to capture conversation data (30 min)
- [ ] Connect to Airtable for incident storage (15 min)  
- [ ] Test end-to-end voice → Airtable flow (15 min)

**Definition of Done**: Voice conversations stored in Airtable dashboard

---

### Sprint 2: Dashboard Enhancement (1 hour)

#### Dashboard Setup
**Assignee**: Data Analyst

**Tasks:**
- [ ] Configure Airtable views for urgency filtering (20 min)
- [ ] Set up Airtable forms for manual incident entry (20 min)
- [ ] Create dashboard sharing links (10 min)
- [ ] Test mobile dashboard access (10 min)

**Definition of Done**: Airtable dashboard ready for demo with sample data

---

### Sprint 3: Testing & Demo Preparation (30 minutes)

#### Demo Preparation
**Assignee**: All Team

**Tasks:**
- [ ] End-to-end voice conversation testing (15 min)
- [ ] Demo script rehearsal (10 min)  
- [ ] Documentation cleanup (5 min)

**Definition of Done**: Demo ready with working voice interface

### Progress Tracking
- **Current Status**: Sprint 0 setup complete, ready for web development
- **Next Milestone**: Create working HTML page with ElevenLabs widget
- **Target Completion**: 4 hours total development time

### Progress Checkpoints
- **Hour 0.5**: Setup complete ✅ COMPLETED
- **Hour 2.5**: Web interface working with voice conversations
- **Hour 3.5**: Dashboard integrated with incident data
- **Hour 4**: Demo ready

### Resume Instructions (Next Session)
1. **Create HTML page** with ElevenLabs widget:
   ```html
   <elevenlabs-convai agent-id="agent_8401kdqtgnnbfx18q1fv460mh7pv"></elevenlabs-convai>
   <script src="https://unpkg.com/@elevenlabs/convai-widget-embed@beta" async type="text/javascript"></script>
   ```
2. **Test voice conversations** in browser
3. **Optional**: Set up webhook to capture data in Airtable
4. **Demo**: Working voice incident reporting

### Scope Protection Rules
1. **Zero infrastructure** - leverage ElevenLabs widget only
2. **Copy-paste approach** - reusable HTML templates
3. **Demo over perfection** - working voice demo beats complex features
4. **Native voice conversations** - ElevenLabs handles all voice processing

### Reusable Hackathon Template
This project creates reusable components for future hackathons:

**Web Template** (`/src/web/`):
- HTML page with embedded ElevenLabs conversational widget
- Mobile-responsive design
- Zero-setup voice conversations

**Integration Templates** (`/src/integrations/`):
- ElevenLabs webhook handlers (optional)
- Airtable data sync utilities
- Email notification scripts

**Dashboard Templates** (`/dashboards/`):
- Airtable base with incident tracking views
- Pre-built views for urgency filtering
- Mobile-responsive layouts

**Deployment**: Open HTML file in browser - working voice AI in 60 seconds