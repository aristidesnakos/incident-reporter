# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Digital Foreman MVP - A voice-activated safety incident reporting system using Telegram bot interface with AI-powered incident triage. The system allows construction workers to report safety incidents via voice messages, automatically classifies them by urgency, and provides real-time dashboard monitoring.

## Architecture

**Serverless Tech Stack:**
- Voice AI: ElevenLabs Conversational AI Agent (native voice-to-voice)
- Bot Platform: Telegram Bot API (via Cloud Functions)
- Backend: Google Cloud Functions (serverless, event-driven)
- Database: Firestore (document database)
- Storage: Cloud Storage (audio conversation logs)
- Dashboard: Airtable (real-time incident tracking)
- Notifications: Telegram-only (emergency alerts via chat)
- Infrastructure: Terraform for repeatable deployments

**Data Flow:**
```
Telegram Bot → Cloud Function Webhook → ElevenLabs Conversational AI Agent → Firestore → Cloud Function → Airtable Dashboard
```

## Key Components

### Cloud Function Architecture
1. **Telegram Voice Handler** (`telegram-voice-handler`): Webhook → download voice file → ElevenLabs agent processing → Firestore storage → urgency-based routing → voice response
2. **Follow-up Scheduler** (`followup-scheduler`): Daily trigger → query unresolved incidents → ElevenLabs follow-up → Telegram delivery
3. **Airtable Sync** (`airtable-sync`): Firestore changes → data transformation → Airtable updates

### Incident Data Model (Firestore)
- Basic incident info: timestamp, user, transcript, audio file URL
- AI classification: urgency, type, location, confidence score
- Status tracking: open/resolved with follow-up messages

## Development Requirements

**Infrastructure (Terraform-managed):**
- Google Cloud Project with Firestore, Cloud Storage, Cloud Functions
- Service accounts with minimal IAM permissions  
- Secret Manager for credential storage

**External Service Setup:**
- Telegram Bot token from @BotFather  
- ElevenLabs Conversational AI Agent ID and API key
- Airtable workspace and base for dashboard

## Development Commands

**Infrastructure Deployment:**
```bash
# One-command infrastructure setup
./deploy.sh [project-id]

# Manual Terraform deployment
cd infrastructure
terraform init
terraform plan -var="project_id=your-project"
terraform apply -var="project_id=your-project"
```

**ElevenLabs Agent Setup:**
```bash
# Create conversational AI agent
cd src/agents
./setup_agent.sh
python3 create_agent.py
```

**Function Development:**
```bash
# Install dependencies for local development
cd src/functions/telegram_handler
pip install -r requirements.txt

# Test individual functions locally (using Functions Framework)
functions-framework --target telegram_handler --debug
```

**Monitoring and Debugging:**
```bash
# View Cloud Function logs
gcloud functions logs read telegram-voice-handler --project=your-project

# Monitor Firestore operations
gcloud firestore operations list --project=your-project

# Check deployment status
terraform output
```

## Project Structure

**Core Architecture (Option 2 Structure):**
- `/src/functions/` - Individual Cloud Functions (Python 3.11)
  - `/telegram_handler/` - Voice message processing
  - `/airtable_sync/` - Real-time dashboard sync  
  - `/followup_scheduler/` - Automated follow-ups
- `/src/agents/` - ElevenLabs agent setup and utilities
- `/src/shared/` - Common utilities (replicated per function)
- `/infrastructure/` - Terraform infrastructure templates
- `/docs/` - Project documentation and sprint planning

**Key Files:**
- `deploy.sh` - One-command infrastructure deployment
- `src/functions/*/main.py` - Individual Cloud Function entry points
- `infrastructure/main.tf` - Complete Terraform infrastructure
- `src/agents/setup_agent.sh` - ElevenLabs conversational agent setup

**Development Process:**
- Terraform infrastructure is deployed first via `./deploy.sh`
- ElevenLabs agent created via `./src/agents/setup_agent.sh`
- Cloud Functions handle serverless voice processing
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

- **End-to-end testing**: Voice message → Telegram → Cloud Function → ElevenLabs → Firestore → Airtable
- **Infrastructure validation**: `terraform plan` and `terraform apply` success
- **Function deployment**: Cloud Functions deployment logs and execution monitoring
- **Integration testing**: Manual testing of Telegram bot responses

**Quality Checks:**
```bash
# Validate Terraform configuration
cd infrastructure && terraform validate

# Check Cloud Function deployment status
gcloud functions describe telegram-voice-handler --region=us-central1

# Monitor function execution logs
gcloud functions logs read telegram-voice-handler --limit=50
```

Refer to docs/TECHNICAL_SPEC.md for detailed Cloud Function specifications and ElevenLabs agent configurations.