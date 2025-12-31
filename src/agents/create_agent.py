#!/usr/bin/env python3
"""
ElevenLabs Conversational AI Agent Creation Script for Digital Foreman

This script creates a conversational AI agent optimized for construction safety incident reporting.
The agent handles voice-to-voice conversations with natural language understanding.
"""

import os
import json
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from safety_manager_tool import get_safety_manager_tool

def create_safety_agent():
    """Create and configure the Digital Foreman safety agent"""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize ElevenLabs client
    elevenlabs = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY")
    )
    
    # Define the agent's conversational prompt
    safety_prompt = """
You are Kathy, a safety companion for construction workers. You help them report incidents through quick voice conversations and notify the Safety Manager immediately.

# Core Behavior
- Speak naturally in short, clear sentences
- Use everyday construction language 
- Show genuine care and urgency when appropriate
- NEVER include reasoning, thinking, or explanations in your speech
- Keep total conversations under 60 seconds
- Always end by notifying the Safety Manager using the webhook tool

# Conversation Flow
1. Acknowledge the report with empathy
2. Ask ONE clarifying question at a time to get complete details
3. Classify urgency and inform worker of next steps
4. Use the notify_safety_manager tool to send incident details
5. Confirm to worker that Safety Manager has been notified

# Your Voice Personality
- Calm but responsive to urgency
- Professional yet approachable
- Patient with stressed workers
- Confident in safety guidance
- Reassuring about follow-up actions

# Incident Classification
Emergency: Active injury, immediate life danger, critical hazards
Urgent: Potential injury risk, equipment failure, significant hazards  
Routine: Safety observations, minor maintenance, suggestions

# Example Exchange
Worker: "Scaffolding looks loose on building 2"
You: "Thanks for reporting that scaffolding issue on building 2. Is anyone working near it right now?"
Worker: "Yeah, there's a crew up there"
You: "Got it. I'm marking this as an emergency since there's a crew at risk. Let me notify the Safety Manager immediately."
[Calls notify_safety_manager tool]
You: "The Safety Manager has been alerted and they'll contact the crew right away to evacuate and inspect the scaffolding. Good catch reporting this."

# Tool Usage
At the end of each incident report, you MUST call the notify_safety_manager webhook tool with these parameters:
- incident_timestamp: Current timestamp of the report
- reporter_name: Name of the worker reporting (ask if not provided)
- incident_location: Specific site location mentioned
- incident_description: Complete summary of what was reported
- urgency_level: "emergency", "urgent", or "routine" 
- incident_type: "injury", "near-miss", "hazard", or "equipment"

# Response Guidelines
- Speak your conversational responses naturally
- Never verbalize your classification process or tool usage
- Always confirm the Safety Manager has been notified
- Provide reassurance about next steps

Remember: Your goal is natural conversation that gathers complete incident details, then uses the webhook tool to immediately notify safety personnel.
"""
    
    try:
        # Create the conversational agent
        response = elevenlabs.conversational_ai.agents.create(
            name="Digital Foreman Safety Agent",
            tags=["safety", "construction", "incident-reporting"],
            conversation_config={
                "tts": {
                    "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel - clear, professional voice
                    "model_id": "eleven_flash_v2",        # Fast, low-latency model
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                    "style": 0.3,  # Professional but warm
                    "use_speaker_boost": True
                },
                "agent": {
                    "first_message": "Hi, this is Rachel from Digital Foreman safety. I'm here to help you report any safety concerns. What's going on?",
                    "prompt": {
                        "prompt": safety_prompt
                    },
                    "language": "en"
                },
                "asr": {  # Automatic Speech Recognition
                    "model": "nova-2",
                    "language": "en"
                },
                "tools": [get_safety_manager_tool()]
            }
        )
        
        agent_id = response.agent_id
        print(f"✅ Digital Foreman Safety Agent created successfully!")
        print(f"🆔 Agent ID: {agent_id}")
        print()
        print("📋 Next Steps:")
        print(f"1. Copy this Agent ID to your web/index.html file:")
        print(f"   agent-id=\"{agent_id}\"")
        print()
        print("2. Test the agent at: https://elevenlabs.io/app/conversational-ai")
        print("3. Open your web application: ../web/index.html")
        print()
        print("🎯 Agent Configuration:")
        print("- Voice: Rachel (professional, clear)")
        print("- Model: eleven_flash_v2 (low latency)")
        print("- Language: English")
        print("- Focus: Construction safety incident reporting")
        print("- Webhook: notify_safety_manager tool enabled")
        
        # Save agent details to file
        agent_info = {
            "agent_id": agent_id,
            "name": "Digital Foreman Safety Agent",
            "voice_id": "21m00Tcm4TlvDq8ikWAM",
            "model": "eleven_flash_v2",
            "created_timestamp": response.created_at if hasattr(response, 'created_at') else None,
            "tags": ["safety", "construction", "incident-reporting"]
        }
        
        with open("agent_info.json", "w") as f:
            json.dump(agent_info, f, indent=2)
        
        print(f"\n💾 Agent details saved to: agent_info.json")
        
        return agent_id
        
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        print()
        print("🔧 Troubleshooting:")
        print("1. Check your ELEVENLABS_API_KEY is set correctly")
        print("2. Verify you have ElevenLabs credits available")
        print("3. Ensure you're on a plan that supports conversational AI")
        return None

def test_agent_connection():
    """Test connection to ElevenLabs API"""
    try:
        load_dotenv()
        elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        
        # Test API connection by listing voices
        voices = elevenlabs.voices.get_all()
        print(f"✅ Connected to ElevenLabs API successfully")
        print(f"📊 Available voices: {len(voices.voices)}")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to ElevenLabs API: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Digital Foreman - ElevenLabs Agent Setup")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("📝 Creating .env file template...")
        with open(".env", "w") as f:
            f.write("ELEVENLABS_API_KEY=your_api_key_here\n")
        print("❗ Please edit .env file with your ElevenLabs API key, then run this script again.")
        exit(1)
    
    # Test API connection first
    print("🔌 Testing ElevenLabs API connection...")
    if not test_agent_connection():
        print("❗ Please check your API key and try again.")
        exit(1)
    
    print()
    print("🤖 Creating conversational AI agent...")
    agent_id = create_safety_agent()
    
    if agent_id:
        print()
        print("🎉 Setup complete! Your Digital Foreman Safety Agent is ready.")
    else:
        print("❌ Agent creation failed. Please check the error messages above.")
        exit(1)