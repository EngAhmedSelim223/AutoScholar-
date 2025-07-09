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
        from config import GROQ_API_KEY, GROQ_MODEL
        from groq import Groq
        
        client = Groq(api_key=GROQ_API_KEY)
        
        # Simple test call
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": "Hello, respond with 'API connection successful'"}],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"🌐 API Test Response: {result}")
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
