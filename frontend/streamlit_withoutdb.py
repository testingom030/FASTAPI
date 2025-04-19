import google.generativeai as genai
import os

# Set your Gemini API Key
GOOGLE_API_KEY = "your-api-key-here"
genai.configure(api_key=GOOGLE_API_KEY)

def analyze_resume(resume_text, job_description):
    prompt = f"""
You are an AI resume analyzer. Analyze the candidate's resume in relation to the given job description.

Extract and return structured JSON with the following fields:
- name
- email
- core_skills (as a list)
- soft_skills (as a list)
- resume_rating (as a percentage)
- improvement_areas
- job_fit_score (as a percentage)
- upskill_suggestions
- skillset_improvements (as a list)

Resume Text:
\"\"\"
{resume_text}
\"\"\"

Job Description:
\"\"\"
{job_description}
\"\"\"

Return JSON only. No explanation.
"""

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    
    # Parse JSON safely
    try:
        result = response.text.strip()
        result = result[result.index("{"):]  # Strip anything before JSON starts
        return json.loads(result)
    except Exception as e:
        return {"error": f"Failed to parse Gemini response: {e}", "raw_response": response.text}
