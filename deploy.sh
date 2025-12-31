#!/bin/bash

# Digital Foreman - Web-Based Setup Script
# Usage: ./deploy.sh

set -e

echo "🚀 Digital Foreman Web-Based Setup"
echo "=================================="

echo ""
echo "📝 Setup checklist:"
echo "1. ✅ ElevenLabs Conversational AI Agent (agent_8401kdqtgnnbfx18q1fv460mh7pv already configured)"
echo "2. ⏳ Create Airtable base for incident tracking"
echo "3. ⏳ Test web interface"
echo ""

# Check if web directory exists
if [ ! -f "src/web/index.html" ]; then
    echo "❌ Web interface not found at src/web/index.html"
    exit 1
fi

echo "🔧 Setting up Airtable base..."
echo ""
echo "Please create an Airtable base with the following structure:"
echo ""
echo "📊 Base Name: 'Digital Foreman Incidents'"
echo ""
echo "📝 Fields:"
echo "   • Incident_ID (Auto-number)"
echo "   • Timestamp (Date & Time)"
echo "   • Reporter (Single line text)"
echo "   • Conversation_Summary (Long text)"
echo "   • Urgency (Single select: Emergency|Urgent|Routine)"
echo "   • Type (Single select: Injury|Near-Miss|Hazard|Equipment)"
echo "   • Location (Single line text)"
echo "   • Status (Single select: Open|In Progress|Resolved)"
echo "   • AI_Confidence (Percent)"
echo "   • Conversation_Link (URL)"
echo ""
echo "📋 Views to create:"
echo "   • Emergency (filter: Urgency = Emergency)"
echo "   • Open Incidents (filter: Status = Open)"
echo "   • Today's Reports (filter: Created today)"
echo "   • Location Summary (group by Location)"
echo ""

echo "Press Enter when you've created the Airtable base..."
read -r

echo ""
echo "🌐 Opening web interface..."
if command -v open >/dev/null 2>&1; then
    open src/web/index.html
elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open src/web/index.html
else
    echo "Please manually open: $(pwd)/src/web/index.html"
fi


echo ""
echo "🧪 Test Instructions:"
echo "1. Click the voice widget in your browser"
echo "2. Say: 'I need to report a safety incident'"
echo "3. Describe an incident like: 'Wet floor in Zone 3, no warning signs'"
echo "4. Verify the AI responds naturally as Rachel"
echo "5. Check classification (Emergency/Urgent/Routine)"
echo ""

echo "📊 Optional: To capture data in Airtable:"
echo "   • Set up webhook endpoint to receive ElevenLabs conversation data"
echo "   • Configure webhook URL in ElevenLabs agent settings"
echo "   • Data will automatically sync to your Airtable base"
echo ""

echo "💰 Estimated cost: <$1 for ElevenLabs usage (free tier: 10,000 chars/month)"
echo ""
echo "✅ Digital Foreman setup complete!"
echo "🎉 Ready for voice-powered safety reporting!"