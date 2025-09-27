#!/usr/bin/env python3
"""
Debug the OpenAI API key issue
"""

import os

def check_environment():
    """Check environment variables"""
    
    print("🔍 Environment Check:")
    print("=" * 30)
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print(f"✅ OPENAI_API_KEY found: {openai_key[:10]}...{openai_key[-5:]}")
        if openai_key.startswith("pplx-"):
            print("❌ This appears to be a Perplexity API key, not OpenAI!")
            print("💡 You need an OpenAI API key starting with 'sk-'")
        elif openai_key.startswith("sk-"):
            print("✅ Looks like a valid OpenAI API key format")
        else:
            print("❌ Unknown API key format")
    else:
        print("❌ OPENAI_API_KEY not found")
    
    openai_model = os.getenv("OPENAI_MODEL")
    print(f"🔧 OPENAI_MODEL: {openai_model or 'Not set (will use default)'}")
    
    # Check working directory
    cwd = os.getcwd()
    print(f"📁 Current working directory: {cwd}")
    
    # Check if .env file exists
    env_files = [".env", "../.env", "../../.env"]
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"📄 Found {env_file}")
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                    if "OPENAI_API_KEY" in content:
                        print(f"✅ {env_file} contains OPENAI_API_KEY")
                    else:
                        print(f"❌ {env_file} does not contain OPENAI_API_KEY")
            except Exception as e:
                print(f"❌ Error reading {env_file}: {e}")
        else:
            print(f"❌ {env_file} not found")

if __name__ == "__main__":
    check_environment()