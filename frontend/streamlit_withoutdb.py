import streamlit as st
import PyPDF2
import json
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = "your-api-key-here"  # Replace this with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Resume Analysis Function Using Gemini
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

Only return valid JSON. Do not include explanations or extra text. The response must start with '{{' and end with '}}'.
"""

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)

    try:
        result_text = response.text.strip()
        result_json = result_text[result_text.index("{"):]  # Remove anything before JSON
        return json.loads(result_json)
    except Exception as e:
        return {
            "error": f"Failed to parse Gemini response: {e}",
            "raw_response": response.text
        }

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Streamlit UI
st.set_page_config(page_title="AI Resume Parser", layout="wide")
tab1, tab2 = st.tabs(["Upload Resume", "View History"])

with tab1:
    st.title("📤 Upload Resume")
    jd = st.text_area("Paste Job Description")
    uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")

    if st.button("Submit") and uploaded_file and jd:
        with st.spinner("Analyzing Resume..."):
            try:
                # Extract text from PDF
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                resume_text = ""
                for page in pdf_reader.pages:
                    resume_text += page.extract_text()

                # Analyze resume with Gemini
                result = analyze_resume(resume_text, jd)
                result["uploaded_file_name"] = uploaded_file.name

                st.success("Analysis complete!")
                st.subheader("🧾 Analysis Output")
                st.json(result)

                if "error" not in result:
                    st.subheader("Formatted Analysis")
                    st.write(f"**Candidate Name:** {result.get('name', 'Not specified')}")
                    st.write(f"**Email:** {result.get('email', 'Not specified')}")
                    st.write(f"**Core Skills:** {', '.join(result.get('core_skills', [])) or 'None'}")
                    st.write(f"**Soft Skills:** {', '.join(result.get('soft_skills', [])) or 'None'}")
                    st.write(f"**Resume Rating:** {result.get('resume_rating', 0)}%")
                    st.write(f"**Improvement Areas:** {result.get('improvement_areas', 'None')}")
                    st.write(f"**Uploaded File:** {result.get('uploaded_file_name', 'Not specified')}")
                    st.write(f"**Job Fit Score:** {result.get('job_fit_score', 0)}%")
                    st.write(f"**Upskill Suggestions:** {result.get('upskill_suggestions', 'None')}")
                    st.write(f"**Skillset Improvements:** {', '.join(result.get('skillset_improvements', [])) or 'None'}")

                # Save to history
                st.session_state.history.append(result)

            except Exception as e:
                st.error(f"Error analyzing resume: {e}")

with tab2:
    st.title("📜 Resume History")

    if st.session_state.history:
        for i, res in enumerate(st.session_state.history[::-1], 1):
            file_name = res.get("uploaded_file_name", f"Resume {i}")
            name = res.get("name", "Unknown Name")
            with st.expander(f"{file_name} - {name}"):
                st.json(res)
                if "error" not in res:
                    st.write(f"**Candidate Name:** {res.get('name', 'Not specified')}")
                    st.write(f"**Email:** {res.get('email', 'Not specified')}")
                    st.write(f"**Core Skills:** {', '.join(res.get('core_skills', [])) or 'None'}")
                    st.write(f"**Soft Skills:** {', '.join(res.get('soft_skills', [])) or 'None'}")
                    st.write(f"**Resume Rating:** {res.get('resume_rating', 0)}%")
                    st.write(f"**Improvement Areas:** {res.get('improvement_areas', 'None')}")
                    st.write(f"**Uploaded File:** {res.get('uploaded_file_name', 'Not specified')}")
                    st.write(f"**Job Fit Score:** {res.get('job_fit_score', 0)}%")
                    st.write(f"**Upskill Suggestions:** {res.get('upskill_suggestions', 'None')}")
                    st.write(f"**Skillset Improvements:** {', '.join(res.get('skillset_improvements', [])) or 'None'}")
    else:
        st.info("No resumes analyzed yet.")
