"""
Simple test script to verify Groq API connection
"""
import os
from dotenv import load_dotenv

# Load .env from project root
project_root = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(project_root, '.env')
print(f"Loading .env from: {env_path}")
load_dotenv(env_path)

# Check what key we loaded
api_key = os.getenv("GROQ_API_KEY")
print(f"API Key loaded: '{api_key}'")
print(f"API Key length: {len(api_key) if api_key else 0}")
print(f"API Key repr: {repr(api_key)}")

if not api_key or api_key == "gsk_...":
    print("\n❌ ERROR: API key is not set or is still the placeholder!")
    print("Please edit .env and add your real Groq API key.")
    exit(1)

# Try to use Groq
try:
    from groq import Groq
    print("\n✓ Groq library imported successfully")
    
    client = Groq(api_key=api_key)
    print("✓ Groq client created")
    
    # Make a simple test call
    print("\nMaking test API call...")
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Say 'Hello World' and nothing else."}],
        model="llama-3.3-70b-versatile",
    )
    
    result = response.choices[0].message.content
    print(f"\n✓ SUCCESS! API Response: {result}")
    
except ImportError as e:
    print(f"\n❌ Groq library not installed: {e}")
except Exception as e:
    print(f"\n❌ API Error: {type(e).__name__}: {e}")
