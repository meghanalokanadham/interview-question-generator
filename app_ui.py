import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

# Load API Key
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Page Title
st.title("🎯 Interview Question Generator")

st.markdown("""
Generate interview questions based on:

- 💼 Job Role
- 📅 Experience Level
""")

# Inputs
role = st.text_input("💼 Enter Role")

experience = st.selectbox(
    "📅 Select Experience",
    [
        "Fresher",
        "1 Year",
        "2 Years",
        "3 Years",
        "5 Years",
        "8+ Years"
    ]
)

# Button
if st.button("🚀 Generate Questions"):

    prompt = f"""
    Generate interview questions for:

    Role: {role}
    Experience: {experience}

    Generate:
    - Exactly 10 Technical Questions
    - Exactly 5 HR Questions

    Return ONLY valid JSON.

    {{
      "technical_questions": [],
      "hr_questions": []
    }}
    """

    try:

        with st.spinner("Generating Questions..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.9
                )
            )

            cleaned_text = response.text.strip()

            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text.replace(
                    "```json",
                    "",
                    1
                )

            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]

            data = json.loads(cleaned_text)

            st.success("✅ Questions Generated Successfully!")

            st.subheader("🔧 Technical Questions")

            for i, q in enumerate(
                data["technical_questions"],
                1
            ):
                st.markdown(f"**{i}.** {q}")

            st.subheader("👥 HR Questions")

            for i, q in enumerate(
                data["hr_questions"],
                1
            ):
                st.markdown(f"**{i}.** {q}")

    except Exception as e:
        st.error(f"❌ Error: {e}")