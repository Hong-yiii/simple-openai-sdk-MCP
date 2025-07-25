#!/usr/bin/env python3
"""
🚀 Amazon Nova Integration Module

Simple integration with Amazon Nova Lite via AWS Bedrock using LiteLLM.
"""

import os
import sys
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NovaIntegration:
    """Handles Amazon Nova Lite integration via AWS Bedrock."""
    
    def __init__(self):
        self.aws_credentials = self._validate_aws_credentials()
        self.nova_model = "litellm/bedrock/amazon.nova-lite-v1:0"
    
    def _validate_aws_credentials(self) -> Dict[str, str]:
        """Validate that required AWS credentials are available."""
        required_vars = [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY", 
            "AWS_REGION_NAME"
        ]
        
        credentials = {}
        missing_vars = []
        
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
            else:
                credentials[var] = value
        
        if missing_vars:
            print(f"❌ Error: Missing required AWS environment variables: {', '.join(missing_vars)}")
            print("Please ensure these are set in your .env file:")
            for var in missing_vars:
                print(f"  {var}=your_value_here")
            sys.exit(1)
        
        print(f"✅ AWS credentials validated for region: {credentials['AWS_REGION_NAME']}")
        return credentials
    
    def get_nova_model(self) -> str:
        """Get the Nova Lite model identifier."""
        return self.nova_model
    
    def print_integration_info(self):
        """Print information about the Nova integration."""
        print("\n🚀 Amazon Nova Integration Active")
        print("=" * 50)
        print(f"🔄 Model: Amazon Nova Lite")
        print(f"🆔 Model ID: {self.nova_model}")
        print(f"🌍 AWS Region: {self.aws_credentials['AWS_REGION_NAME']}")
        print(f"💡 Provider: AWS Bedrock via LiteLLM")
        print(f"📝 Description: Multimodal, fast, very low cost")
        print("-" * 50)

def validate_nova_setup() -> Tuple[bool, Optional[NovaIntegration]]:
    """
    Validate Nova setup and return integration instance.
    
    Returns:
        Tuple of (is_valid, nova_integration_instance)
    """
    try:
        nova = NovaIntegration()
        return True, nova
    except SystemExit:
        return False, None
    except Exception as e:
        print(f"❌ Error initializing Nova integration: {e}")
        return False, None

# Test function for development
if __name__ == "__main__":
    print("Testing Nova Integration...")
    is_valid, nova = validate_nova_setup()
    
    if is_valid and nova:
        print("✅ Nova integration test successful!")
        print(f"Nova model: {nova.get_nova_model()}")
    else:
        print("❌ Nova integration test failed!") 