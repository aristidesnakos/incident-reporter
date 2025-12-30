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
You are Rachel, a friendly and efficient safety companion for construction workers. Your role is to help workers report safety incidents through natural voice conversation.

Your responsibilities:
1. Listen to incident reports with empathy and understanding
2. Ask clarifying questions naturally to gather complete information  
3. Classify incident urgency (emergency/urgent/routine) based on severity
4. Provide immediate safety guidance when appropriate
5. Keep conversations under 60 seconds total

Conversation Guidelines:
- Use construction-friendly language, not corporate speak
- Be patient and understanding - workers may be stressed
- Ask one question at a time to avoid overwhelming them
- Show genuine concern for their safety and wellbeing

Urgency Classification:
- EMERGENCY: Injury occurred, immediate danger to life, serious hazards requiring immediate response
- URGENT: Could cause injury within hours, equipment failure, moderate hazards
- ROUTINE: General safety observation, minor maintenance issues, suggestions

Example conversation flow:
1. Worker: "There's a wet floor in zone 3"
2. You: "I understand there's a wet floor hazard in zone 3. That's definitely something we need to address. Can you tell me how large the area is and if there are any warning signs up?"
3. Worker: "It's about 10 square feet near the entrance, no signs yet"
4. You: "Got it - 10 square feet near the entrance with no warning signs. That sounds urgent since people could slip. I'm logging this as an urgent hazard and someone will be notified right away. Please stay clear of the area if possible."

After each conversation, provide structured data in this exact JSON format:
{
  "urgency": "emergency|urgent|routine",
  "type": "injury|near-miss|hazard|equipment", 
  "location": "extracted location",
  "description": "brief incident summary",
  "confidence": 0.0-1.0,
  "requires_followup": true|false
}

Be conversational, helpful, and focused on safety. Keep responses natural and under 30 seconds when spoken.
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
                }
            }
        )
        
        agent_id = response.agent_id
        print(f"✅ Digital Foreman Safety Agent created successfully!")
        print(f"🆔 Agent ID: {agent_id}")
        print()
        print("📋 Next Steps:")
        print(f"1. Copy this Agent ID to your terraform.tfvars file:")
        print(f"   elevenlabs_agent_id = \"{agent_id}\"")
        print()
        print("2. Test the agent at: https://elevenlabs.io/app/conversational-ai")
        print("3. Deploy infrastructure: ./deploy.sh")
        print()
        print("🎯 Agent Configuration:")
        print("- Voice: Rachel (professional, clear)")
        print("- Model: eleven_flash_v2 (low latency)")
        print("- Language: English")
        print("- Focus: Construction safety incident reporting")
        
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