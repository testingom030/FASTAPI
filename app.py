import streamlit as st
import PyPDF2
import json

# Simulate or import your LLM resume analysis logic here
def analyze_resume(resume_text, job_description):
    # This function should return a dictionary
    # Replace this with actual LLM/Gemini/OpenAI logic
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "core_skills": ["Python", "Machine Learning", "FastAPI"],
        "soft_skills": ["Teamwork", "Communication"],
        "resume_rating": 85,
        "improvement_areas": "Add more recent projects.",
        "uploaded_file_name": "resume.pdf",
        "job_fit_score": 78,
        "upskill_suggestions": "Learn Docker and cloud deployment.",
        "skillset_improvements": ["Docker", "Cloud Architecture"]
    }

# Init session state
if "history" not in st.session_state:
    st.session_state.history = []

# Page config
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

                # Call your resume parser
                result = analyze_resume(resume_text, jd)
                result["uploaded_file_name"] = uploaded_file.name

                # Display analysis
                st.success("Analysis complete!")
                st.subheader("🧾 Analysis Output")
                st.json(result)

                # Formatted display
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

                # Save to session history
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
