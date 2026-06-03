!pip install -q google-generativeai
import os
import google.generativeai as genai
os.environ["GEMINI_API_KEY"] = 'AQ.Ab8RN6LzKp5iDTN9Xij7QU6KkKi60-Be-TbCdX7YXEikmgiqtg'

genai.configure(api_key=os.environ["GEMINI_API_KEY"]
model = genai.GenerativeModel("gemini-1.5-flash")
