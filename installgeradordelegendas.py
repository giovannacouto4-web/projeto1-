!pip install -q google-generativeai
import os
import google.generativeai as genai
os.environ["GEMINI_API_KEY"] = 'AQ.Ab8RN6Ij49N8f5xoPgaa3Pg7i7BDjSpL91S0SBPqiCdBNHQaJg'

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
