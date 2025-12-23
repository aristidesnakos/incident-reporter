# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Digital Foreman MVP - A voice-activated safety incident reporting system using Telegram bot interface with AI-powered incident triage. The system allows construction workers to report safety incidents via voice messages, automatically classifies them by urgency, and provides real-time dashboard monitoring.

## Architecture

**No-Code Tech Stack:**
- Workflow Engine: n8n (self-hosted on Cloud Run)
- Bot Platform: Telegram Bot API (via n8n Telegram nodes)
- AI: Vertex AI Gemini 1.5 Flash (via n8n HTTP nodes)
- Database: Firestore (via n8n Google Firestore nodes)
- Storage: Cloud Storage (via n8n Google Cloud Storage nodes)
- Dashboard: Airtable (via n8n Airtable nodes)
- Notifications: Gmail/email (via n8n Gmail nodes) - simpler than SMS
- Infrastructure: Terraform for repeatable deployments

**Data Flow:**
```
Telegram Bot → n8n Webhook → n8n Workflows → Vertex AI → Firestore → Airtable Dashboard
```

## Key Components

### n8n Workflow Architecture
1. **Main Voice Processing Workflow**: Telegram webhook → download voice file → audio conversion → Vertex AI transcription → incident classification → Firestore storage → urgency-based routing (email/Telegram/log) → confirmation message
2. **Follow-up Automation Workflow**: Scheduled trigger (24h) → query unresolved incidents → send follow-up messages → update follow-up counts
3. **Dashboard Sync Workflow**: Firestore changes webhook → data transformation → Airtable record updates

### Incident Data Model (Firestore)
- Basic incident info: timestamp, user, transcript, audio file URL
- AI classification: urgency, type, location, confidence score
- Status tracking: open/resolved with follow-up messages

## Development Requirements

**Infrastructure (Terraform-managed):**
- Google Cloud Project with Firestore, Cloud Storage, Cloud Run
- n8n instance deployed on Cloud Run with PostgreSQL backend
- Service accounts with minimal IAM permissions

**External Service Setup:**
- Telegram Bot token from @BotFather  
- Gmail account for email alerts (simpler than SMS setup)
- Airtable workspace and base for dashboard

**No-Code Development Process:**
- Primary development happens in n8n visual workflow editor
- Terraform templates handle infrastructure provisioning
- Airtable serves as ready-made dashboard (no custom frontend needed)
- Minimal custom code reduces security attack surface

## Development Process

**Infrastructure Setup (30 minutes):**
- Deploy Terraform templates for GCP resources
- Configure n8n instance on Cloud Run  
- Set up external services (Telegram bot, Twilio, Airtable)

**No-Code Development Sprints:**
- Sprint 1: Core n8n workflows (voice processing, AI classification, routing)
- Sprint 2: Follow-up automation and smart triage tuning
- Sprint 3: Airtable dashboard integration and data sync
- Sprint 4: Testing, performance optimization, demo preparation

**Key Development Activities:**
- Visual workflow creation in n8n editor (no traditional coding)
- AI prompt engineering for incident classification
- Airtable base design for dashboard views
- Terraform infrastructure updates as needed

Refer to TECHNICAL_SPEC.md for detailed n8n node configurations and workflow specifications.