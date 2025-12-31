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
open src/web/index.html

# Serve locally for HTTPS (required for microphone access)
python3 -m http.server 8000
# Then visit http://localhost:8000/src/web/
```

**ElevenLabs Agent Setup:**
```bash
cd src/agents

# Install Python dependencies
pip install -r requirements.txt

# Set up environment and create agent
./setup_agent.sh
python3 create_agent.py

# Agent will output ID to paste into src/web/index.html
```

**Code Quality:**
```bash
# No formal linting/testing commands - this is a rapid prototype
# Manual testing via browser and voice interface
```

## Project Structure

**Simple Web Architecture:**
- `/src/web/` - Single HTML page with embedded ElevenLabs widget
- `/src/agents/` - ElevenLabs agent setup and utilities
- `/src/webhook/` - Optional webhook for data capture (if needed)
- `/docs/` - Project documentation and sprint planning

**Key Files:**
- `src/web/index.html` - Complete web application with embedded ElevenLabs widget
- `src/agents/create_agent.py` - Agent creation script (creates conversational AI agent)
- `src/agents/safety_manager_tool.py` - Webhook tool configuration for Safety Manager notifications
- `src/agents/requirements.txt` - Python dependencies for agent creation
- `src/agents/setup_agent.sh` - Environment setup script
- `src/agents/agent_info.json` - Generated agent configuration (after creation)

**Current Agent Configuration:**
- Agent ID: `agent_8401kdqtgnnbfx18q1fv460mh7pv` (configured in index.html)
- Voice: Rachel (professional, clear)
- LLM: Google Gemini 2.5 Flash (via ElevenLabs integration)
- Tools: Safety Manager webhook notification

**Development Workflow:**
1. Test existing agent via `src/web/index.html` (agent already created)
2. For new agent: run `./setup_agent.sh` then `python3 create_agent.py` 
3. Update `agent-id` attribute in `index.html` with new agent ID
4. Test voice interface through browser (requires microphone permissions)

## Documentation Discipline

**CRITICAL**: Claude Code must consult and update these documents during development:

### Before Starting Any Task:
1. **Read docs/SPRINT_PLAN.md** - Current sprint status, timeline, and priorities  
2. **Check docs/DEVELOPMENT_CHECKLIST.md** - Technical implementation status

### During Development:
- **Update docs/DEVELOPMENT_CHECKLIST.md** immediately after completing technical tasks
- **Update docs/SPRINT_PLAN.md** progress tracking in real-time

### Documentation Commands:
```bash
# Run documentation discipline check before starting work  
./enforce-docs.sh

# Key files to consult in Claude Code:
read docs/SPRINT_PLAN.md          # Sprint goals and timeline
read docs/DEVELOPMENT_CHECKLIST.md # Task status and completion tracking
```

**Enforcement Script:**
- Always run `./enforce-docs.sh` before starting development (if exists)
- Update `docs/DEVELOPMENT_CHECKLIST.md` immediately after completing tasks

**Note**: This is a hackathon MVP project focused on rapid prototyping with minimal documentation overhead.

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

## Important Notes for Claude Code

**Project Status**: This is a completed hackathon submission for the ElevenLabs Challenge. The core functionality is working:
- Live demo at: https://aristidesnakos.github.io/incident-reporter/src/web/
- ElevenLabs Conversational AI agent is fully configured and functional
- Voice-to-voice safety incident reporting works end-to-end

**Development Focus**: Any future development should prioritize:
1. Testing the existing voice interface 
2. Understanding the agent configuration in `create_agent.py`
3. Maintaining the simple, working architecture
4. Consulting sprint docs before making changes

**Code Quality**: Run Python code through basic linting if modifying agent scripts. The `safety_manager_tool.py` has been formatted to meet line length requirements.