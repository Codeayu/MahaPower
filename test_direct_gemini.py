#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('c:/Users/Lenovo/Documents/GitHub/MahaPower/core')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Setup Django
django.setup()

try:
    import google.generativeai as genai
    from django.conf import settings
    
    # Configure Gemini directly
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    # Test with a simple, safe prompt
    test_prompt = "Please provide 3 benefits of starting a small vegetable garden in a rural village in Maharashtra, India."
    
    response = model.generate_content(test_prompt)
    
    print("✅ Direct Gemini Test Successful!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()