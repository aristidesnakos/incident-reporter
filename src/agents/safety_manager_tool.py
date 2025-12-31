#!/usr/bin/env python3
"""
Safety Manager Webhook Tool Definition for ElevenLabs Agent

This module defines the webhook tool configuration that enables the
Digital Foreman safety agent to automatically notify the Safety Manager
when incident reports are completed.
"""

import json

def get_safety_manager_tool():
    """
    Returns the webhook tool configuration for notifying the Safety Manager
    
    Returns:
        dict: Complete tool configuration for ElevenLabs agent
    """
    return {
        "type": "webhook",
        "name": "notify_safety_manager",
        "description": (
            "Notifies the Safety Manager with incident details after "
            "completing an incident report. This sends an email to the "
            "appropriate safety personnel based on the incident type and urgency."
        ),
        "disable_interruptions": False,
        "force_pre_tool_speech": "auto",
        "assignments": [],
        "tool_call_sound": None,
        "tool_call_sound_behavior": "auto",
        "execution_mode": "immediate",
        "api_schema": {
            "url": "https://yourdomain.app.n8n.cloud/webhook/ga4e1821-a11y-808x-ada-0fed7223g5321",
            "method": "POST",
            "path_params_schema": [],
            "query_params_schema": [],
            "request_body_schema": {
                "id": "body",
                "type": "object",
                "description": (
                    "The notify_safety_manager tool sends incident details to the "
                    "appropriate safety personnel. It ensures the Safety Manager "
                    "and relevant team members are immediately informed of "
                    "construction site safety incidents."
                ),
                "properties": [
                    {
                        "id": "incident_timestamp",
                        "type": "string",
                        "value_type": "llm_prompt",
                        "description": (
                            "The timestamp when the safety incident occurred "
                            "or was reported"
                        ),
                        "dynamic_variable": "",
                        "constant_value": "",
                        "enum": None,
                        "is_system_provided": False,
                        "required": True
                    },
                    {
                        "id": "reporter_name", 
                        "type": "string",
                        "value_type": "llm_prompt",
                        "description": (
                            "The name of the construction worker who reported "
                            "this safety incident"
                        ),
                        "dynamic_variable": "",
                        "constant_value": "",
                        "enum": None,
                        "is_system_provided": False,
                        "required": True
                    },
                    {
                        "id": "incident_location",
                        "type": "string", 
                        "value_type": "llm_prompt",
                        "description": (
                            "The specific location on the construction site "
                            "where the incident occurred"
                        ),
                        "dynamic_variable": "",
                        "constant_value": "",
                        "enum": None,
                        "is_system_provided": False,
                        "required": True
                    },
                    {
                        "id": "incident_description",
                        "type": "string",
                        "value_type": "llm_prompt", 
                        "description": (
                            "A detailed description of the safety incident "
                            "that was reported by the worker"
                        ),
                        "dynamic_variable": "",
                        "constant_value": "",
                        "enum": None,
                        "is_system_provided": False,
                        "required": True
                    },
                    {
                        "id": "urgency_level",
                        "type": "string",
                        "value_type": "llm_prompt",
                        "description": (
                            "The classified urgency level of the incident: "
                            "emergency, urgent, or routine"
                        ),
                        "enum": ["emergency", "urgent", "routine"],
                        "dynamic_variable": "",
                        "constant_value": "",
                        "is_system_provided": False,
                        "required": True
                    },
                    {
                        "id": "incident_type", 
                        "type": "string",
                        "value_type": "llm_prompt",
                        "description": (
                            "The type of safety incident: injury, near-miss, "
                            "hazard, or equipment"
                        ),
                        "enum": ["injury", "near-miss", "hazard", "equipment"], 
                        "dynamic_variable": "",
                        "constant_value": "",
                        "is_system_provided": False,
                        "required": True
                    },
                    {
                        "id": "safety_manager_email",
                        "type": "string",
                        "value_type": "constant",
                        "description": "Email address of the Safety Manager to be notified",
                        "constant_value": "6901why4w0@mozmail.com",
                        "dynamic_variable": "",
                        "enum": None,
                        "is_system_provided": False,
                        "required": True
                    },
                    {
                        "id": "tool",
                        "type": "string",
                        "value_type": "constant",
                        "description": "Tool identifier for safety incident notification",
                        "constant_value": "notify_safety_manager",
                        "dynamic_variable": "",
                        "enum": None,
                        "is_system_provided": False,
                        "required": True
                    }
                ],
                "required": False,
                "value_type": "llm_prompt"
            },
            "request_headers": [],
            "auth_connection": None
        },
        "response_timeout_secs": 20,
        "dynamic_variables": {
            "dynamic_variable_placeholders": {}
        }
    }

def get_tool_json():
    """
    Returns the tool configuration as a formatted JSON string
    
    Returns:
        str: JSON representation of the tool configuration
    """
    return json.dumps(get_safety_manager_tool(), indent=2)

if __name__ == "__main__":
    print("🔧 Safety Manager Webhook Tool Configuration")
    print("=" * 50)
    print()
    print("📋 Tool JSON Configuration:")
    print(get_tool_json())
    print()
    print("💡 Usage:")
    print("- Import get_safety_manager_tool() in create_agent.py")
    print("- Add to agent's tools array during creation")
    print("- Configure webhook URL for your environment")
