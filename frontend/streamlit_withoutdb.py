import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_gemini_response(resume_text, jd_text, file_name):
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

    prompt = f"""
Act like a highly experienced ATS system.

Compare the resume and job description below. Output a structured JSON like this:

{{
  "name": "Extracted Name from Resume",
  "email": "Extracted Email",
  "core_skills": ["skill1", "skill2"],
  "soft_skills": ["skillA", "skillB"],
  "resume_rating": 0-100 (based on relevance to job),
  "improvement_areas": "short paragraph",
  "uploaded_file_name": "{file_name}",
  "job_fit_score": score from -5 to +5 (based on fit),
  "upskill_suggestions": "missing keywords or skills to learn"
}}

Resume:
{resume_text}

Job Description:
{jd_text}
    """

    response = model.generate_content(prompt)
    
    try:
        data = json.loads(response.text)
    except:
        st.warning("⚠️ Gemini response wasn't valid JSON. Here's the raw output:")
        return response.text

    return data


def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response as per below structure
{
  "name": "Abhimanyu Ajudiya",
  "email": "abhimanyuajudiya@gmail.com",
  "core_skills": [
    "Python",
    "Docker",
    "REST APIs"
  ],
  "soft_skills": [
    "Communication",
    "Teamwork"
  ],
  "resume_rating": 60,
  "improvement_areas": "Improve LinkedIn presence, project descriptions.",
  "uploaded_file_name": "Abhimanyu.pdf",
  "job_fit_score": -3.25,
  "upskill_suggestions": "Resume may be missing relevant job keywords: string"
}

"""

## streamlit app

with st.sidebar:
    st.title("Smart ATS for Resumes")
    st.subheader("About")
    st.write("This sophisticated ATS project, developed with Gemini Pro and Streamlit, seamlessly incorporates advanced features including resume match percentage, keyword analysis to identify missing criteria, and the generation of comprehensive profile summaries, enhancing the efficiency and precision of the candidate evaluation process for discerning talent acquisition professionals.")
    
    st.markdown("""
    - [Streamlit](https://streamlit.io/)
    - [Gemini Pro](https://deepmind.google/technologies/gemini/#introduction)
    - [makersuit API Key](https://makersuite.google.com/)
    - [Github](https://github.com/OMCHOKSI108/End-To-End-Resume-ATS-Tracking-LLM-Project-With-Google-Gemini-Pro) Repository
                
    """)
    
    add_vertical_space(5)
    st.write("Made with ❤ by OM CHOKSI.")
    
    


st.title("Smart Application Tracking System")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")
if submit:
    if uploaded_file is not None and jd:
        resume_text = input_pdf_text(uploaded_file)
        file_name = uploaded_file.name
        result = get_gemini_response(resume_text, jd, file_name)

        st.subheader("Analysis Result")

        if isinstance(result, dict):
            st.json(result)
        else:
            st.code(result)  # fallback if it's just raw text
    else:
        st.warning("Please upload a resume and provide a job description.")