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
    from home.gemini_service import gemini_service
    print("✅ Google Gemini service loaded successfully!")
    print(f"📱 Model: {gemini_service.model.model_name}")
    
    # Test a simple generation
    test_analysis = gemini_service.generate_work_analysis(
        work_type="Dairy Farming",
        work_type_mr="दूध व्यवसाय",
        district="Amravati",
        district_mr="अमरावती",
        taluka="Amravati",
        taluka_mr="अमरावती",
        gram_panchayat="Rajapeth",
        gram_panchayat_mr="राजापेठ",
        sector="Agriculture",
        sector_mr="कृषी",
        is_specialty=False,
        language="en"
    )
    
    print("🧠 AI Analysis Generated:")
    print(f"Overview: {test_analysis.get('overview', 'N/A')}")
    print(f"Why Suitable: {len(test_analysis.get('why_suitable', []))} points")
    print(f"Business Potential: {len(test_analysis.get('business_potential', []))} points")
    print("✅ Google Gemini AI integration working perfectly!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()