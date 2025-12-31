# Digital Foreman MVP

Voice-activated safety incident reporting system using ElevenLabs Conversational AI and simple web interface.

## Quick Start

1. **Setup External Services**
   ```bash
   # Create ElevenLabs agent, Airtable base
   cd src/agents && ./setup_agent.sh
   ```

2. **Run Setup Script**
   ```bash
   ./deploy.sh
   ```

3. **Test Voice Conversations**
   - Click the voice widget to start conversation
   - Report safety incidents naturally via voice
   - Check incidents in Airtable dashboard (optional)

## Architecture

**Simple Web Stack:**
- Voice AI: ElevenLabs Conversational AI Widget
- Frontend: Single HTML page
- Backend: Optional webhook for data capture
- Dashboard: Airtable
- Infrastructure: Zero complexity

**Project Structure:**
```
src/
├── web/                # HTML page with ElevenLabs widget
│   └── index.html           # Main web interface
├── agents/             # ElevenLabs agent setup
└── webhook/            # Optional data capture (if needed)

docs/                  # Documentation  
```

## Documentation

See `docs/` directory for detailed documentation:
- `docs/TECHNICAL_SPEC.md` - Architecture details and setup guide
- `docs/DEVELOPMENT_CHECKLIST.md` - Technical task tracking
- `docs/SPRINT_PLAN.md` - Project timeline and progress
- `docs/PRD.md` - Product requirements

## Cost

Estimated cost: <$1 for 4-hour development sprint.

Perfect for hackathons and rapid prototyping!