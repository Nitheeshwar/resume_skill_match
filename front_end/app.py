import streamlit as st
import requests

st.title("AI Resume Matcher")

option = st.radio("Choose Resume Option", ['Existing', 'Upload New'])

if option == 'Existing':
    resume_id = st.text_input("Enter Resume ID")
else:
    uploaded_file = st.file_uploader("Upload Resume", type=['pdf'])

job_description = st.text_area("Paste Job Description")

if st.button("Match"):
    if option == 'Existing' and not resume_id:
        st.error("Please enter a resume ID.")
    elif option == 'Upload New' and not uploaded_file:
        st.error("Please upload a resume.")
    else:
        files = {}
        if option == 'Upload New':
            files['resume'] = uploaded_file
        data = {
            'resume_id': resume_id if option == 'Existing' else '',
            'jobDescription': job_description
        }
        response = requests.post("http://localhost:8000/match/", data=data, files=files)
        if response.ok:
            result = response.json()
            st.success(f"Match Score: {result['match_score']}%")
            st.write("Missing Keywords:", result['missing_keywords'])
            st.write("Resume ID:", result['resume_id'])
        else:
            st.error("Something went wrong.")

if st.button("Generate Cover Letter"):
    if option == 'Existing' and not resume_id:
        st.error("Please enter a resume ID.")
    elif option == 'Upload New' and not uploaded_file:
        st.error("Please upload a resume.")
    else:
        files = {}
        if option == 'Upload New':
            files['resume'] = uploaded_file
        data = {
            'resume_id': resume_id if option == 'Existing' else '',
            'jobDescription': job_description
        }
    response = requests.post("http://localhost:8000/generate_cover/", data=data)
    st.subheader("📄 Cover Letter")
    st.code(response.json()["cover_letter"])

if st.button("Suggest Improvements"):
    if option == 'Existing' and not resume_id:
        st.error("Please enter a resume ID.")
    elif option == 'Upload New' and not uploaded_file:
        st.error("Please upload a resume.")
    else:
        files = {}
        if option == 'Upload New':
            files['resume'] = uploaded_file
        data = {
            'resume_id': resume_id if option == 'Existing' else '',
            'jobDescription': job_description
        }
    response = requests.post("http://localhost:8000/suggest/", data=data)
    st.subheader("💡 Suggestions")
    st.markdown(response.json()["suggestions"])

