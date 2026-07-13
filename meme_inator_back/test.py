import json

from openai import OpenAI
from openai.types import ModerationCreateResponse
import os
client = OpenAI()

# Check if API key is set
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    print("❌ OPENAI_API_KEY not set!")
else:
    print(f"✅ API key found (starts with: {api_key[:10]}...)")
    
    # Try with explicit key
    client = OpenAI(api_key=api_key)
    try:
        response = client.moderations.create(
            model="omni-moderation-latest",
            input="test"
        )
        print("✅ Success!")
    except Exception as e:
        print(f"Error: {e}")




response:ModerationCreateResponse = client.moderations.create(
    model="omni-moderation-latest",
    input="the heck 😈",
)

print(json.dumps(response.model_dump(), indent=2))
