# Gemini API Environment Setup Guide

## Setup Instructions

### 1. Get Your Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

### 2. Configure Environment Variables

#### Option A: Using `.env` file (Recommended for development)
1. Open `.env` file in the `ngo_project` folder
2. Replace `your_gemini_api_key_here` with your actual API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. Save the file

#### Option B: Using System Environment Variables (for production)
**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your_actual_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your_actual_api_key_here
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your_actual_api_key_here"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Setup
Run this test command to verify your setup:
```bash
python -c "from config import GEMINI_API_KEY; print('✓ API Key loaded successfully')"
```

## File Structure

- `.env` - Your local environment variables (Git ignored)
- `.env.example` - Template for environment variables (shared in repo)
- `config.py` - Central configuration management
- `requirements.txt` - Python dependencies

## Security Notes

⚠️ **Important:** Never commit your `.env` file with actual API keys to version control!

- `.env` is automatically ignored by Git (see `.gitignore`)
- Use `.env.example` as a template for other developers
- Keep your API key private and never share it publicly

## Troubleshooting

If you get an error about GEMINI_API_KEY:
1. Ensure `.env` file exists in the `ngo_project` folder
2. Verify the API key is correctly set (without quotes in the .env file)
3. Make sure `python-dotenv` is installed: `pip install python-dotenv`
4. Restart your Python environment after adding the .env file

## Using the API in Your Code

Import configuration in your Python files:
```python
from config import GEMINI_API_KEY
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Your prompt here")
```
