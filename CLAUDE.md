# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Digital Foreman MVP - A web-based voice-activated safety incident reporting system with AI-powered incident triage. The system allows construction workers to report safety incidents via voice conversations through a simple web interface, automatically classifies them by urgency, and provides real-time dashboard monitoring.

## Architecture

**Simple Web Stack:**
- Voice AI: ElevenLabs Conversational AI Widget (native voice-to-voice)
- Frontend: Single HTML page (mobile-responsive)
- Backend: Optional webhook for data capture
- Dashboard: Airtable (real-time incident tracking)
- Infrastructure: Zero infrastructure required

**Data Flow:**
```
Web Page → ElevenLabs Conversational AI Widget → [Optional: Webhook] → Airtable Dashboard
```

## Key Components

### Web Interface
1. **HTML Page** (`src/web/index.html`): Simple web page with embedded ElevenLabs widget
2. **ElevenLabs Widget**: Voice-to-voice conversational AI for incident reporting
3. **Optional Webhook**: Captures conversation data and sends to Airtable

### Incident Data Model (Airtable)
- Basic incident info: timestamp, reporter, conversation summary
- AI classification: urgency, type, location, confidence score
- Status tracking: open/in progress/resolved

## Development Requirements

**No Infrastructure Required:**
- Just a web browser and text editor
- Optional: Simple web server for webhook (if data capture needed)

**External Service Setup:**
- ElevenLabs Conversational AI Agent ID and API key
- Airtable workspace and base for dashboard

## Development Commands

**Web Development:**
```bash
# Open HTML page in browser
open /path/to/src/web/index.html

# Serve locally (optional)
python3 -m http.server 8000
# Then visit http://localhost:8000/src/web/
```

**ElevenLabs Agent Setup:**
```bash
# Create conversational AI agent
cd src/agents
./setup_agent.sh
python3 create_agent.py
```

**Optional Webhook Development:**
```bash
# For data capture integration (if needed)
cd src/webhook
python3 app.py  # Simple Flask/FastAPI server
```

## Project Structure

**Simple Web Architecture:**
- `/src/web/` - Single HTML page with embedded ElevenLabs widget
- `/src/agents/` - ElevenLabs agent setup and utilities
- `/src/webhook/` - Optional webhook for data capture (if needed)
- `/docs/` - Project documentation and sprint planning

**Key Files:**
- `src/web/index.html` - Main web interface with ElevenLabs widget
- `src/agents/setup_agent.sh` - ElevenLabs conversational agent setup
- `src/agents/create_agent.py` - Agent configuration script

**Development Process:**
- ElevenLabs agent created via `./src/agents/setup_agent.sh`
- Open `src/web/index.html` in browser for immediate voice interface
- Optional webhook setup for Airtable data capture
- Airtable serves as ready-made dashboard

## Documentation Discipline

**CRITICAL**: Claude Code must consult and update these documents during development:

### Before Starting Any Task:
1. **Read docs/SPRINT_PLAN.md** - Current sprint status, timeline, and priorities
2. **Read docs/TECHNICAL_SPEC.md** - Architecture and integration requirements  
3. **Check docs/DEVELOPMENT_CHECKLIST.md** - Technical implementation status

### During Development:
- **Update docs/DEVELOPMENT_CHECKLIST.md** immediately after completing technical tasks
- **Update docs/SPRINT_PLAN.md** progress tracking in real-time
- **Check docs/PRD.md** for requirements validation when encountering blockers

### After Completing Sprints/Milestones:
- **Update docs/SPRINT_PLAN.md** with completion status and next priorities
- **Update docs/TECHNICAL_SPEC.md** if architecture evolves
- **Update docs/PRD.md** if requirements shift

### Documentation Commands:
```bash
# Run documentation discipline check before starting work
./enforce-docs.sh

# Key files to consult in Claude Code:
read docs/SPRINT_PLAN.md          # Sprint goals and timeline
read docs/TECHNICAL_SPEC.md       # Architecture and integration requirements  
read docs/DEVELOPMENT_CHECKLIST.md # Task status and completion tracking
```

**Enforcement Script:**
- Always run `./enforce-docs.sh` before starting development
- Updates `docs/DEVELOPMENT_CHECKLIST.md` immediately after completing tasks
- Consult `docs/TECHNICAL_SPEC.md` or `docs/PRD.md` when encountering blockers

**Failure to consult docs = incomplete implementation**

## Testing and Quality

**No formal test suite exists** - this is a rapid prototype/MVP project focused on demonstrating voice AI capabilities. Quality assurance happens through:

- **End-to-end testing**: Web page → ElevenLabs widget → voice conversation → response
- **Browser compatibility**: Test on Chrome, Safari, Firefox, mobile browsers
- **Voice quality**: Test microphone input and speaker output
- **Integration testing**: Manual testing of voice conversation flows

**Quality Checks:**
```bash
# Test web page locally
open src/web/index.html

# Test with local server (for HTTPS if needed)
python3 -m http.server 8000

# Validate HTML
# Use browser dev tools to check for console errors
```

Refer to docs/TECHNICAL_SPEC.md for detailed ElevenLabs agent configurations and widget integration.