"""
Claude Integration Module for Simple MCP

This module handles integration with Anthropic's Claude model via LiteLLM.
"""

import os
from typing import Tuple, Any, Optional

def validate_claude_setup() -> Tuple[bool, Optional[Any]]:
    """
    Validate Claude API setup and return integration module.
    
    Returns:
        Tuple[bool, Optional[Any]]: (is_valid, integration_module)
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        return False, None
    
    return True, ClaudeIntegration()

class ClaudeIntegration:
    """Handles Claude model integration via LiteLLM."""
    
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.model_name = "claude-3-opus-20240229"  # Latest Claude model
    
    def get_model(self) -> str:
        """
        Get the Claude model configuration.
        
        Returns:
            str: Model identifier for LiteLLM
        """
        return f"claude/{self.model_name}"
    
    def print_integration_info(self) -> None:
        """Print information about the Claude integration."""
        print("\n🤖 Claude Integration Information:")
        print(f"  • Model: {self.model_name}")
        print("  • Provider: Anthropic")
        print("  • Integration: LiteLLM")
        print("  • Status: Active\n") 