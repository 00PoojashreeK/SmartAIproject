"""
Quick test script to verify Gemini API is working
Run this before submitting to hackathon
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

print("🔍 Testing Gemini API Setup...\n")

# Load environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Check API key
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env")
    print("📝 Add it to .env file first")
    exit(1)

if api_key == "your_gemini_api_key_here":
    print("❌ ERROR: GEMINI_API_KEY is still placeholder")
    print("📝 Replace with your actual API key in .env")
    exit(1)

print("✅ API Key loaded")

# Configure API
try:
    genai.configure(api_key=api_key)
    print("✅ Gemini API configured")
except Exception as e:
    print(f"❌ Failed to configure API: {e}")
    exit(1)

# Test model initialization
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("✅ Model initialized")
except Exception as e:
    print(f"❌ Failed to initialize model: {e}")
    exit(1)

# Test API call
try:
    print("\n🧪 Testing API call...")
    response = model.generate_content("Say 'Hello! Chatbot is working' in one sentence.")
    print(f"✅ API Response: {response.text}\n")
except Exception as e:
    print(f"❌ API call failed: {e}")
    print(f"Details: {str(e)}")
    exit(1)

print("=" * 50)
print("✅ ALL TESTS PASSED - READY FOR SUBMISSION")
print("=" * 50)
print("\nRun the app with: streamlit run app.py")
