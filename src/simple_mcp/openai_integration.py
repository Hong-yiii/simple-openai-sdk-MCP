"""
OpenAI Integration Module for Simple MCP

This module handles integration with OpenAI's models via LiteLLM.
"""

import os
from typing import Tuple, Any, Optional

def validate_openai_setup() -> Tuple[bool, Optional[Any]]:
    """
    Validate OpenAI API setup and return integration module.
    
    Returns:
        Tuple[bool, Optional[Any]]: (is_valid, integration_module)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return False, None
    
    return True, OpenAIIntegration()

class OpenAIIntegration:
    """Handles OpenAI model integration via LiteLLM."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = "gpt-4o-mini"  # Using GPT-4o-mini model
    
    def get_model(self) -> str:
        """
        Get the OpenAI model configuration.
        
        Returns:
            str: Model identifier for LiteLLM
        """
        return f"openai/{self.model_name}"
    
    def print_integration_info(self) -> None:
        """Print information about the OpenAI integration."""
        print("\n🤖 OpenAI Integration Information:")
        print(f"  • Model: {self.model_name}")
        print("  • Provider: OpenAI")
        print("  • Integration: LiteLLM")
        print("  • Status: Active\n")
