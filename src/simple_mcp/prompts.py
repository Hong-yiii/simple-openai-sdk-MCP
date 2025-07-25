"""
Module containing system prompts and prompt generation logic for the MCP agents.
"""

import os
from typing import Optional
from datetime import datetime

def get_prompt() -> str:
    """
    Generate a prompt for the agent to use.
    
    Returns:
        str: The complete system prompt with all variables substituted.
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f'''You are an agent designed to help the user with their query, please answer according to the following instructions:

Current Date and Time: {current_time}


'''
