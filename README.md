# Digital Foreman - Voice-Powered Safety Reporting

🏆 **ElevenLabs Challenge Submission** - Voice-driven safety incident reporting for construction using ElevenLabs Conversational AI + Google Gemini 2.5 Flash

## 🚀 Live Demo

**🌐 Hosted Application**: https://aristidesnakos.github.io/incident-reporter/src/web/

> ⚠️ **Demo Period**: Active during hackathon judging (limited time to prevent usage charges)
> 
> 🎙️ **Voice Required**: Click the voice widget and speak naturally about a safety incident

## 🎯 Challenge Alignment

### ElevenLabs Integration ✅
- **Primary Interface**: ElevenLabs Conversational AI widget
- **Voice-to-Voice**: Complete conversation without typing
- **Natural Interaction**: Professional voice persona for construction safety
- **Real-time Processing**: Immediate voice responses

### Google Cloud AI Integration ✅
- **LLM Backend**: Google Gemini 2.5 Flash powering conversation logic
- **Intelligent Classification**: Automatic urgency assessment (Emergency/Urgent/Routine)
- **Context Awareness**: Construction-specific terminology understanding
- **Natural Language Processing**: Sophisticated incident analysis

## 🏗️ Use Case: Construction Safety

**Problem**: Construction workers avoid reporting safety incidents due to complex forms and time constraints.

**Solution**: Natural voice conversation with AI safety coordinator - just talk, no typing.

**Value**: Faster reporting = better safety outcomes = fewer accidents.

## 🎮 How to Use

1. **Visit**: https://aristidesnakos.github.io/incident-reporter/src/web/
2. **Allow Microphone**: Grant browser permission when prompted
3. **Click Voice Widget**: Start conversation with AI safety coordinator
4. **Speak Naturally**: Describe your safety incident as if talking to a human
5. **Get Classification**: AI automatically categorizes urgency and provides guidance

### Example Conversation:
```
You: "Hey, we had a close call today with the crane"
AI: "I'd like to help you report this safely. Can you tell me what happened with the crane?"
You: "The operator was lifting a load and it swung close to where Mike was working"
AI: "That sounds concerning. Was anyone injured, and was Mike able to move out of the way safely?"
...
AI: "I'm classifying this as URGENT due to the crane safety risk. I'll make sure this gets immediate attention."
```

## 💻 Technical Stack

- **Frontend**: Responsive HTML5 with embedded ElevenLabs widget
- **Voice AI**: ElevenLabs Conversational Agent (`agent_8401kdqtgnnbfx18q1fv460mh7pv`)
- **LLM**: Google Gemini 2.5 Flash (integrated via ElevenLabs)
- **Hosting**: GitHub Pages (free, reliable, HTTPS for microphone access)
- **Mobile**: Fully responsive design for job site use

## 🔧 Local Development

### Prerequisites
- Web browser with microphone access
- Python 3 and pip (for creating your own ElevenLabs agent)
- ElevenLabs API key (if creating new agent)

### Option 1: Use Existing Demo
```bash
# Clone repository
git clone https://github.com/aristidesnakos/incident-reporter.git
cd incident-reporter

# Open in browser
open src/web/index.html
# OR serve locally for HTTPS (required for microphone)
python3 -m http.server 8000
# Then visit: http://localhost:8000/src/web/
```

### Option 2: Create Your Own Agent
```bash
# Clone repository
git clone https://github.com/aristidesnakos/incident-reporter.git
cd incident-reporter/src/agents

# Install Python dependencies
pip install -r requirements.txt

# Run setup script
./setup_agent.sh

# Create agent with safety manager webhook tool
python3 create_agent.py

# Follow prompts to:
# 1. Add your ElevenLabs API key
# 2. Create new conversational agent
# 3. Update src/web/index.html with your agent ID
```

### File Structure
```
├── src/web/index.html          # Complete web application
├── src/agents/                 # ElevenLabs agent setup
│   ├── agent_info.json         # Current agent configuration
│   ├── create_agent.py         # Agent creation script
│   ├── safety_manager_tool.py  # Webhook tool for Safety Manager notifications
│   ├── setup_agent.sh          # Automated setup script
│   └── requirements.txt        # Python dependencies
├── docs/                       # Project documentation
│   ├── DEVELOPMENT_CHECKLIST.md # Technical implementation status
│   └── SPRINT_PLAN.md          # Sprint goals and timeline
├── CLAUDE.md                   # Claude Code guidance file
├── LICENSE                     # MIT open source license
└── README.md                   # This file
```

## 🛡️ Usage Protection

**For Hackathon Judges**: The demo is live and ready for testing!

**Cost Management**: 
- Demo enabled during judging period
- ElevenLabs usage monitored to prevent overages
- Webhook integration for Safety Manager notifications
- Time-limited access to prevent abuse after hackathon

## 🏅 Why This Wins

### 🎯 Perfect Challenge Fit
- **Voice-First**: Primary interface is conversation, not clicks
- **ElevenLabs + Google AI**: Seamless integration of both required technologies
- **Real Conversations**: Not just text-to-speech, actual back-and-forth dialog
- **Practical Application**: Construction safety has immediate ROI

### 💡 Technical Excellence
- **Simple & Stable**: Clean implementation that works reliably
- **Mobile-Optimized**: Perfect for construction job sites
- **Zero Infrastructure**: GitHub Pages hosting = no server complexity
- **Professional UX**: Matches construction industry expectations
- **Webhook Integration**: Safety Manager notification system via webhook tools

### 🚀 Demo Impact
- **Immediate Understanding**: Safety problem is universally recognized
- **Obvious Value**: Voice reporting is clearly better than forms
- **Judges Can Test**: Public demo with working voice interaction
- **Memorable**: Real conversation with AI is impressive

## 📋 Submission Details

- **Challenge**: ElevenLabs Challenge - Conversational Voice AI
- **Repository**: https://github.com/aristidesnakos/incident-reporter
- **Live Demo**: https://aristidesnakos.github.io/incident-reporter/src/web/
- **Demo Video**: [YouTube URL - Coming Soon]
- **License**: MIT (Open Source)

## 🔗 Links

- **Live Application**: https://aristidesnakos.github.io/incident-reporter/src/web/
- **Source Code**: https://github.com/aristidesnakos/incident-reporter
- **ElevenLabs**: https://elevenlabs.io/
- **Google Gemini**: https://deepmind.google/technologies/gemini/

---

**Built for ElevenLabs Challenge 2025** 🎙️ **Voice-First Future** ⚡ **Construction Safety Innovation**

> 🤖 Generated with Claude Code - Co-Authored-By: Claude <noreply@anthropic.com>