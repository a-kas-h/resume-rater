from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import base64
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model=genai.GenerativeModel('gemini-2.5-pro')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        
        img_byte_array = io.BytesIO()
        first_page.save(img_byte_array, format='JPEG')
        img_byte_array = img_byte_array.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_array).decode(),
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Resume Review", page_icon=":guardsman:")
st.header("Resume Review")
input_text = st.text_area("Job Description", key="input")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf", key="file_uploader")

if uploaded_file is not None:
    st.write("File uploaded successfully!")

submit1 = st.button("Describe my resume")
submit2 = st.button("How can my resume be improved")
submit3 = st.button("Percentage match with job description")

input_prompt1 = """
Provide a detailed summary of the strengths, themes, and skills showcased in this resume. 
Highlight any technical proficiencies, soft skills, and domain-specific expertise. Also mention how well the resume is structured for ATS (Applicant Tracking Systems), 
including formatting, keyword usage, and readability. Provide an ATS compatibility score.
"""

input_prompt2 = """
Analyze the attached resume and suggest improvements in terms of structure, clarity, grammar, keyword optimization, and relevance to job roles. 
Highlight missing elements such as measurable achievements, action verbs, or ATS-compatible formatting. 
Provide an ATS compatibility score and explain which changes would increase the score.
"""

input_prompt3 = """
Compare this resume against the provided job description. Calculate a percentage match based on skills, keywords, experience, and qualifications. 
Also include an ATS score reflecting how well the resume would perform in an automated screening for this role. 
Suggest specific improvements to increase the match score.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a pdf")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a pdf")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a pdf")