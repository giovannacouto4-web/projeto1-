!pip install -q google-generativeai
import os
import google.generativeai as genai
os.environ["GEMINI_API_KEY"] = 'Ab8RN6IbNfgDcgDc1jim4bbKV2eVKHZg-jiHwvgJtunUxtE2ZQ'

genai.configure(api_key=os.environ["GEMINI_API_KEY"]
model = genai.GenerativeModel("gemini-1.5-flash")
