# Digital Foreman MVP

Voice-activated safety incident reporting system using ElevenLabs Conversational AI and serverless architecture.

## Quick Start

1. **Setup External Services**
   ```bash
   # Create Telegram bot, ElevenLabs agent, Airtable base
   cd src/agents && ./setup_agent.sh
   ```

2. **Deploy Infrastructure**
   ```bash
   ./deploy.sh your-project-id
   ```

3. **Test the System**
   - Send voice message to your Telegram bot
   - Check incidents appear in Airtable dashboard
   - Monitor Cloud Functions logs

## Architecture

**Serverless Tech Stack:**
- Voice AI: ElevenLabs Conversational AI Agent
- Backend: Google Cloud Functions  
- Database: Firestore
- Dashboard: Airtable
- Notifications: Telegram

**Project Structure:**
```
src/
├── functions/          # Individual Cloud Functions
│   ├── telegram_handler/    # Voice processing
│   ├── airtable_sync/       # Real-time sync
│   └── followup_scheduler/  # Automated follow-ups
├── agents/             # ElevenLabs agent setup
└── shared/            # Common utilities

infrastructure/         # Terraform templates
docs/                  # Documentation  
```

## Documentation

See `docs/` directory for detailed documentation:
- `docs/TECHNICAL_SPEC.md` - Architecture details
- `docs/external-services-setup.md` - Setup guide  
- `docs/DEVELOPMENT_CHECKLIST.md` - Task tracking

## Cost

Estimated cost: <$5 for 12-hour development sprint.

Perfect for hackathons and rapid prototyping!