# 🚀 Hackathon Submission - Setup Without Virtual Environment

## Quick Setup (No Virtual Environment)

### 1. Install Dependencies Globally
```bash
pip install streamlit google-generativeai python-dotenv pandas folium plotly pyperclip
```

### 2. Get Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### 3. Add API Key to .env
Edit `.env` file in the `ngo_project` folder:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Run the Application
```bash
cd ngo_project
streamlit run app.py
```

## Project Structure
```
ngo_project/
├── app.py              # Main Streamlit app
├── chatbot.py          # AI Chatbot module ✅
├── auth.py             # Authentication
├── dashboard.py        # Dashboard module
├── upload.py           # Dataset upload
├── ai_model.py         # AI model page
├── map.py              # Map visualization
├── report.py           # Report generation
├── .env                # API Key (Git ignored)
├── .env.example        # Template for .env
├── dataset.csv         # Data file
└── requirements.txt    # Dependencies
```

## Features
- ✅ AI Disaster Chatbot with Gemini API
- ✅ Dataset upload & analysis
- ✅ Interactive maps
- ✅ AI-powered insights
- ✅ Report generation

## Troubleshooting

**Error: GEMINI_API_KEY not configured**
- Ensure `.env` file exists in `ngo_project` folder
- API key must be set correctly without quotes

**Error: Module not found**
- Run: `pip install -r requirements.txt`

**Chatbot not responding**
- Check API key validity
- Ensure dataset.csv is uploaded first
- Check internet connection

## For Judges
- Login page included for security
- Dataset upload in "Upload Dataset" section
- AI features in "AI Model" and "Chatbot" tabs
- Maps show disaster hotspots
- Reports auto-generate analysis

Ready to submit! 🎯
