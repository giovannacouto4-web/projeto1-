!pip install -q google-generativeai
import os
import google.generativeai as genai
os.environ["GEMINI_API_KEY"] = 'AQ.Ab8RN6L1CNYAn4PfztBK6gJHkABXZTiwZz1SV4eUUfpCY1FGkg'

genai.configure(api_key=os.environ["GEMINI_API_KEY"]

