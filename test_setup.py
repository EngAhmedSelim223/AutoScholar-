#!/usr/bin/env python3
"""
Quick test to validate the AutoScholar setup
"""

def test_imports():
    """Test if all required packages can be imported."""
    try:
        import groq
        print("✅ groq package imported successfully")
        
        import PyPDF2
        print("✅ PyPDF2 package imported successfully")
        
        from dotenv import load_dotenv
        print("✅ python-dotenv package imported successfully")
        
        print("\n📋 Testing project modules...")
        
        from utils import extract_text_from_pdf, call_groq_api
        print("✅ utils module imported successfully")
        
        from phd_student_agent import PhDStudentAgent
        print("✅ phd_student_agent module imported successfully")
        
        from postdoc_agent import PostdocAgent
        print("✅ postdoc_agent module imported successfully")
        
        from professor_agent import ProfessorAgent
        print("✅ professor_agent module imported successfully")
        
        print("\n🎉 All imports successful! AutoScholar is ready to run.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_api_connection():
    """Test if GROQ API connection works."""
    try:
        from utils import call_groq_api
        # Test single call
        result = call_groq_api("Hello, respond with 'API connection successful'")
        print(f"🌐 API Test Response: {result}")
        # Test batch call
        batch_results = call_groq_api([
            "Say 'Batch test 1'", "Say 'Batch test 2'", "Say 'Batch test 3'"
        ], batch_mode=True)
        print(f"🌐 Batch API Test Responses: {batch_results}")
        print("✅ GROQ API connection successful!")
        return True
    except Exception as e:
        print(f"❌ API connection error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 AUTOSCHOLAR SETUP VALIDATION")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        print("\n" + "=" * 50)
        # Test API
        api_ok = test_api_connection()
        
        if api_ok:
            print("\n🎉 Setup validation completed successfully!")
            print("You can now run: python main.py")
        else:
            print("\n⚠️  API connection failed. Please check your GROQ API key.")
    else:
        print("\n⚠️  Some packages are missing. Please install requirements.")
