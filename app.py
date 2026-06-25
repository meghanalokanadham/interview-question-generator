from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

role = input("Enter Role: ")

experience = input("Enter Experience: ")

prompt = f"""
Generate interview questions for:

Role: {role}
Experience: {experience}

Generate:
- 10 Technical Questions
- 5 HR Questions

Return ONLY valid JSON in this format:

{{
  "technical_questions": [
  ],
  "hr_questions": [
  ]
}}
"""
try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.5
        )
    )

    cleaned_text = response.text.strip()

    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text.replace("```json", "", 1)

    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3]

    data = json.loads(cleaned_text)

    print("\n=== Technical Questions ===\n")

    for i, q in enumerate(data["technical_questions"], 1):
        print(f"{i}. {q}")

    print("\n=== HR Questions ===\n")

    for i, q in enumerate(data["hr_questions"], 1):
        print(f"{i}. {q}")

except Exception as e:
    print("Error occurred:")
    print(e)


#print(prompt)  # Temporary, just to verify the prompt