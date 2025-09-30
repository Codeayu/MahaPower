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
    
    # Test the exact prompt we're using
    test_prompt = """You are a helpful business guidance advisor for rural development in Maharashtra, India. Please provide practical, location-specific guidance for village-level entrepreneurs and small business activities.

Please provide guidance for starting "Dairy Farming" in Rajapeth village, Amravati taluka, Amravati district, Maharashtra.

This is part of the Agriculture sector. Please share:

Why this is suitable for Rajapeth:
- Local opportunities and advantages
- Available resources in the area
- Community benefits

Growth possibilities:
- Market potential in the region
- Expected income for small scale
- Investment requirements

Please provide helpful, practical advice for rural Maharashtra communities."""
    
    response = model.generate_content(test_prompt)
    
    print("✅ Specific Business Prompt Test Successful!")
    print(f"Response: {response.text[:500]}...")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    if hasattr(e, 'response'):
        print(f"Response candidates: {e.response.candidates}")
    import traceback
    traceback.print_exc()