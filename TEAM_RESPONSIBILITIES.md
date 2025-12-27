# Team Responsibilities
## Digital Foreman MVP - No-Code Team Structure

### Product Manager
**Primary Focus**: Project coordination, stakeholder management, scope protection

**Key Responsibilities**:
- [ ] Sprint coordination and progress tracking
- [ ] Scope protection - ensure no-code approach maintained
- [ ] Demo preparation and pitch deck
- [ ] External service coordination (Telegram, ElevenLabs, Gmail, Airtable)
- [ ] Template documentation for reusability
- [ ] Final go/no-go decisions for demo

**Daily Tasks**:
- Monitor progress against 24-hour timeline
- Remove blockers for team members
- Ensure MVP scope and no-code principles maintained
- Coordinate external service setup

**Deliverables**:
- Updated sprint planning documents
- Demo script and pitch deck
- Reusable template documentation
- External service setup guides

---

### Infrastructure Engineer (formerly Backend Engineer)
**Primary Focus**: Terraform infrastructure, n8n deployment, Cloud Run management

**Key Responsibilities**:
- [ ] Terraform template development and deployment
- [ ] n8n instance setup on Cloud Run
- [ ] PostgreSQL database configuration for n8n
- [ ] Google Cloud service account management
- [ ] Secret Manager configuration
- [ ] Cloud Run scaling and monitoring

**Technical Ownership**:
- Infrastructure as Code (Terraform modules)
- n8n platform deployment and maintenance
- GCP resource management
- Security and IAM configurations

**Daily Tasks**:
- Infrastructure monitoring and optimization
- n8n instance maintenance
- Terraform template refinement
- Cloud cost monitoring

---

### Workflow Engineer (formerly Backend + AI Engineer)
**Primary Focus**: n8n conversational AI workflow development, voice integration nodes

**Key Responsibilities**:
- [ ] Conversational voice processing workflow creation in n8n
- [ ] Telegram webhook and voice response node configuration
- [ ] Vertex AI Gemini conversational prompt integration
- [ ] ElevenLabs text-to-speech HTTP node setup
- [ ] Firestore read/write node setup
- [ ] Gmail email alert node configuration
- [ ] Follow-up automation workflow with voice responses
- [ ] Error handling nodes and conversational flow logging

**Technical Ownership**:
- All n8n conversational workflows and node configurations
- AI conversation design and prompt engineering within n8n HTTP nodes
- ElevenLabs voice synthesis integration and personality tuning
- Workflow error handling and conversation monitoring
- Voice processing pipeline optimization for natural interactions

**Daily Tasks**:
- Visual conversational workflow development in n8n editor
- Voice synthesis node configuration and testing
- AI conversation prompt refinement and personality development
- Workflow performance optimization for sub-3-second responses

---

### Dashboard Engineer (formerly Frontend Engineer)  
**Primary Focus**: Airtable base design, data sync workflows, mobile optimization

**Key Responsibilities**:
- [ ] Airtable base setup with incident tracking and conversation transcript views
- [ ] n8n → Airtable sync workflow development for conversational data
- [ ] View configuration for urgency filtering and voice interaction history
- [ ] Mobile app experience optimization for conversation playback
- [ ] CSV export workflow setup including voice transcripts
- [ ] Real-time data sync monitoring for conversational incidents

**Technical Ownership**:
- Airtable base architecture and views
- Data transformation workflows
- Mobile dashboard experience
- Real-time sync reliability

**Daily Tasks**:
- Airtable base design and testing
- Sync workflow development in n8n
- Mobile experience validation
- Data visualization optimization

---

### Template Architect (formerly Technical Lead)
**Primary Focus**: Reusable template creation, documentation, architecture decisions

**Key Responsibilities**:
- [ ] Overall no-code architecture design
- [ ] Terraform module template creation
- [ ] n8n workflow template export and documentation
- [ ] Airtable base template creation
- [ ] One-command deployment script development
- [ ] Security best practices for no-code stack

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
**Time**: Every 4 hours during development sprint
**Duration**: 10 minutes  
**Format**:
- What did you complete in the last block?
- What will you work on next?
- Any blockers or dependencies?

#### Configuration Reviews (All Engineers)
- All n8n workflows must be tested before activation
- Focus on functionality and error handling
- Security credential validation
- Performance impact assessment for workflow executions

#### Testing Responsibilities
- **Infrastructure Engineer**: Infrastructure deployment testing, scalability
- **Workflow Engineer**: n8n conversational workflow testing, ElevenLabs voice quality validation, Gemini conversation accuracy  
- **Dashboard Engineer**: Airtable sync testing, mobile compatibility, conversation transcript display
- **Template Architect**: End-to-end conversational integration testing, template validation

#### Demo Preparation (All Team Members)
- **Product Manager**: Script, timing, and conversational demo narrative
- **Infrastructure Engineer**: System monitoring and backup infrastructure
- **Workflow Engineer**: Test conversation data seeding, workflow reliability, voice quality optimization
- **Dashboard Engineer**: Airtable view optimization and mobile testing for conversation display
- **Template Architect**: Backup plans and troubleshooting guides for voice integration

### Decision Making Process (Accelerated for 24-hour timeline)

#### No-Code Technical Decisions
1. **Individual level**: n8n node configurations, Airtable view design
2. **Template Architect approval**: Architecture changes, new service integrations
3. **Product Manager approval**: Scope changes, external service additions
4. **Quick consensus**: Major architectural decisions (15-minute decision window)

#### Escalation Path (Accelerated)
**Level 1**: Direct team member collaboration (immediate)
**Level 2**: Template Architect consultation (within 1 hour)
**Level 3**: Product Manager decision (within 2 hours)
**Level 4**: Team huddle for consensus (within 4 hours)

### Communication Guidelines
- **Slack**: Real-time communication and quick decisions
- **n8n UI**: Workflow documentation and node comments
- **Terraform**: Infrastructure documentation via comments
- **Airtable**: Data structure and view documentation

### Template Handoff Requirements
Each team member must create reusable templates:
- **Infrastructure Engineer**: Documented Terraform modules with variables
- **Workflow Engineer**: Exported n8n workflows with setup instructions
- **Dashboard Engineer**: Airtable base template with view configurations
- **Template Architect**: One-command deployment guide and troubleshooting

### Reusable Template Goals
- **5-minute setup**: Future hackathons can deploy conversational AI infrastructure in under 5 minutes
- **30-minute customization**: Conversational voice processing workflows adaptable for new use cases
- **Documented APIs**: Clear integration points for ElevenLabs, Gemini, and other AI services
- **Mobile-ready**: Airtable templates work immediately on mobile devices with conversation playback
- **Voice-first**: Templates optimized for natural conversation flows and voice interactions

This template-first approach ensures rapid deployment for future conversational AI projects while maintaining the current MVP development speed.