#!/usr/bin/env python3
"""
Nova Integration Module for Simple MCP

This module handles integration with Amazon's Nova model via LiteLLM.
"""

import os
from typing import Tuple, Any, Optional

def validate_nova_setup() -> Tuple[bool, Optional[Any]]:
    """
    Validate Nova/AWS setup and return integration module.
    
    Returns:
        Tuple[bool, Optional[Any]]: (is_valid, integration_module)
    """
    required_vars = [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_REGION_NAME"
    ]
    
    # Check all required environment variables
    for var in required_vars:
        if not os.getenv(var):
            return False, None
    
    return True, NovaIntegration()

class NovaIntegration:
    """Handles Nova model integration via LiteLLM."""
    
    def __init__(self):
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.region = os.getenv("AWS_REGION_NAME")
        self.model_name = "amazon.nova-lite-v1:0"
    
    def get_model(self) -> str:
        """
        Get the Nova model configuration.
        
        Returns:
            str: Model identifier for LiteLLM
        """
        return f"bedrock/{self.model_name}"
    
    def print_integration_info(self) -> None:
        """Print information about the Nova integration."""
        print("\n🤖 Nova Integration Information:")
        print(f"  • Model: {self.model_name}")
        print(f"  • Region: {self.region}")
        print("  • Provider: Amazon AWS")
        print("  • Integration: LiteLLM")
        print("  • Status: Active\n") 