# Team Responsibilities
## Digital Foreman MVP - Serverless Conversational AI Team Structure

### Product Manager
**Primary Focus**: Project coordination, stakeholder management, scope protection

**Key Responsibilities**:
- [ ] Sprint coordination and progress tracking
- [ ] Scope protection - ensure serverless architecture maintained
- [ ] Demo preparation and pitch deck
- [ ] External service coordination (Telegram, ElevenLabs, Gmail, Airtable)
- [ ] Template documentation for reusability
- [ ] Final go/no-go decisions for demo

**Daily Tasks**:
- Monitor progress against 12-hour timeline
- Remove blockers for team members
- Ensure MVP scope and serverless principles maintained
- Coordinate external service setup

**Deliverables**:
- Updated sprint planning documents
- Demo script and pitch deck
- Reusable template documentation
- External service setup guides

---

### Infrastructure Engineer
**Primary Focus**: Terraform infrastructure, Cloud Functions deployment, GCP management

**Key Responsibilities**:
- [ ] Terraform template development and deployment
- [ ] Cloud Functions setup and configuration
- [ ] Firestore database configuration
- [ ] Google Cloud service account management
- [ ] Secret Manager configuration
- [ ] Cloud Scheduler setup for follow-ups

**Technical Ownership**:
- Infrastructure as Code (Terraform modules)
- Serverless Cloud Functions deployment
- GCP resource management
- Security and IAM configurations

**Daily Tasks**:
- Infrastructure monitoring and optimization
- Cloud Functions deployment and maintenance
- Terraform template refinement
- Cloud cost monitoring

---

### AI Engineer (formerly Workflow Engineer)
**Primary Focus**: ElevenLabs Conversational AI agent, Cloud Function voice processing

**Key Responsibilities**:
- [ ] ElevenLabs Conversational AI agent creation and configuration
- [ ] Safety prompt engineering and conversation design
- [ ] Voice personality tuning (Rachel voice configuration)
- [ ] Cloud Function development for voice processing pipeline
- [ ] Telegram webhook integration
- [ ] Emergency routing logic implementation
- [ ] Follow-up automation via ElevenLabs agent

**Technical Ownership**:
- ElevenLabs agent configuration and prompt engineering
- Cloud Function voice processing pipeline
- AI conversation design and safety classification
- Voice quality optimization and testing

**Daily Tasks**:
- ElevenLabs agent testing and refinement
- Cloud Function development and deployment
- Voice conversation flow optimization
- AI response time optimization (<2 seconds)

---

### Backend Engineer
**Primary Focus**: Firestore integration, Airtable sync, Gmail alerts

**Key Responsibilities**:
- [ ] Firestore database schema design
- [ ] Cloud Function for Airtable real-time sync
- [ ] Gmail API integration for emergency alerts
- [ ] Incident data transformation and storage
- [ ] Follow-up scheduling Cloud Function
- [ ] API integration error handling

**Technical Ownership**:
- Firestore database operations
- External API integrations (Airtable, Gmail)
- Data transformation and sync reliability
- Backend Cloud Function error handling

**Daily Tasks**:
- Database schema optimization
- API integration development
- Data sync testing and monitoring
- Backend function performance optimization

---

### Dashboard Engineer
**Primary Focus**: Airtable base design, mobile optimization

**Key Responsibilities**:
- [ ] Airtable base setup with incident tracking views
- [ ] Real-time data sync monitoring
- [ ] View configuration for urgency filtering
- [ ] Mobile app experience optimization
- [ ] CSV export functionality
- [ ] Dashboard user experience testing

**Technical Ownership**:
- Airtable base architecture and views
- Mobile dashboard experience
- Data visualization optimization
- Real-time sync monitoring

**Daily Tasks**:
- Airtable base design and testing
- Mobile experience validation
- Data visualization optimization
- Sync reliability monitoring

---

### Template Architect (Technical Lead)
**Primary Focus**: Reusable template creation, documentation, architecture decisions

**Key Responsibilities**:
- [ ] Overall serverless architecture design
- [ ] Terraform module template creation
- [ ] Cloud Function template export and documentation
- [ ] Airtable base template creation
- [ ] One-command deployment script development
- [ ] Security best practices for serverless stack

**Technical Ownership**:
- Template architecture and reusability
- Documentation and setup guides
- Security implementation across all platforms
- Performance monitoring strategy

**Daily Tasks**:
- Template architecture documentation
- Cross-platform integration testing
- Security configuration validation
- Deployment automation refinement

---

### Cross-Team Responsibilities

#### Daily Check-ins (All Team Members)
**Time**: Every 2 hours during development sprint
**Duration**: 5 minutes  
**Format**:
- What did you complete in the last block?
- What will you work on next?
- Any blockers or dependencies?

#### Code Reviews (All Engineers)
- All Cloud Functions must be tested before deployment
- Focus on functionality and error handling
- Security credential validation
- Performance impact assessment

#### Testing Responsibilities
- **Infrastructure Engineer**: Infrastructure deployment testing, scalability
- **AI Engineer**: ElevenLabs agent testing, voice quality validation, conversation accuracy  
- **Backend Engineer**: API integration testing, data sync reliability
- **Dashboard Engineer**: Airtable sync testing, mobile compatibility
- **Template Architect**: End-to-end integration testing, template validation

#### Demo Preparation (All Team Members)
- **Product Manager**: Script, timing, and demo narrative
- **Infrastructure Engineer**: System monitoring and backup infrastructure
- **AI Engineer**: Test conversation data seeding, agent reliability, voice quality optimization
- **Backend Engineer**: Data pipeline testing and emergency alert verification
- **Dashboard Engineer**: Airtable view optimization and mobile testing
- **Template Architect**: Backup plans and troubleshooting guides

### Decision Making Process (Accelerated for 12-hour timeline)

#### Technical Decisions
1. **Individual level**: Cloud Function configurations, Airtable view design
2. **Template Architect approval**: Architecture changes, new service integrations
3. **Product Manager approval**: Scope changes, external service additions
4. **Quick consensus**: Major architectural decisions (10-minute decision window)

#### Escalation Path (Accelerated)
**Level 1**: Direct team member collaboration (immediate)
**Level 2**: Template Architect consultation (within 30 minutes)
**Level 3**: Product Manager decision (within 1 hour)
**Level 4**: Team huddle for consensus (within 2 hours)

### Communication Guidelines
- **Slack**: Real-time communication and quick decisions
- **Google Cloud Console**: Function logs and monitoring
- **Terraform**: Infrastructure documentation via comments
- **Airtable**: Data structure and view documentation

### Template Handoff Requirements
Each team member must create reusable templates:
- **Infrastructure Engineer**: Documented Terraform modules with variables
- **AI Engineer**: ElevenLabs agent configuration scripts and setup instructions
- **Backend Engineer**: Cloud Function templates with deployment guides
- **Dashboard Engineer**: Airtable base template with view configurations
- **Template Architect**: One-command deployment guide and troubleshooting

### Reusable Template Goals
- **3-minute setup**: Future hackathons can deploy conversational AI infrastructure in under 3 minutes
- **15-minute customization**: Voice processing pipeline adaptable for new use cases
- **Documented APIs**: Clear integration points for ElevenLabs and other AI services
- **Mobile-ready**: Airtable templates work immediately on mobile devices
- **Voice-first**: Templates optimized for natural conversation flows

This template-first approach ensures rapid deployment for future conversational AI projects while maintaining the current MVP development speed.

### Key Architecture Differences from n8n Approach

**No n8n Components**:
- No visual workflow editor
- No PostgreSQL database for n8n
- No Cloud Run instance for n8n
- No n8n node configurations

**New Serverless Components**:
- ElevenLabs Conversational AI Agent (native voice-to-voice)
- Google Cloud Functions (3 functions total)
- Direct API integrations
- Event-driven architecture

**Benefits**:
- 80% faster development (12h vs 24h)
- 67% lower cost (~$5 vs $15)
- Higher reliability for demos
- Simpler debugging and monitoring