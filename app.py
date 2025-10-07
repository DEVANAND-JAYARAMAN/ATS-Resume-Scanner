import streamlit as st
import sqlite3
from resume_parser import ResumeParser
from ats_scorer import ATSScorer
from database import Database
import plotly.express as px
import pandas as pd

def main():
    st.set_page_config(page_title="ATS Resume Scanner", layout="wide")
    
    st.title("🎯 ATS Resume Scanner")
    st.subheader("AI-Powered Intelligent Recruitment System")
    
    # Initialize components
    db = Database()
    parser = ResumeParser()
    scorer = ATSScorer()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", 
                               ["Upload Resume", "Job Matching", "Analytics", "Database"])
    
    if page == "Upload Resume":
        upload_resume_page(parser, scorer, db)
    elif page == "Job Matching":
        job_matching_page(scorer, db)
    elif page == "Analytics":
        analytics_page(db)
    elif page == "Database":
        database_page(db)

def upload_resume_page(parser, scorer, db):
    st.header("📄 Resume Upload & Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Upload Resume", type=['pdf', 'docx', 'txt'])
        job_description = st.text_area("Job Description", height=200)
        
        if st.button("Analyze Resume") and uploaded_file and job_description:
            with st.spinner("Processing..."):
                # Parse resume
                resume_data = parser.parse_resume(uploaded_file)
                
                # Calculate ATS score
                ats_score = scorer.calculate_score(resume_data, job_description)
                
                # Store in database
                db.store_resume(resume_data, ats_score)
                
                st.success(f"Resume processed! ATS Score: {ats_score['total_score']:.1f}%")
    
    with col2:
        if uploaded_file and job_description:
            resume_data = parser.parse_resume(uploaded_file)
            ats_score = scorer.calculate_score(resume_data, job_description)
            
            # Display results
            st.subheader("📊 ATS Analysis Results")
            
            # Score breakdown
            fig = px.bar(
                x=list(ats_score.keys())[:-1],
                y=list(ats_score.values())[:-1],
                title="Score Breakdown"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Resume details
            st.subheader("📋 Extracted Information")
            st.json(resume_data)

def job_matching_page(scorer, db):
    st.header("🎯 Job Matching")
    
    job_desc = st.text_area("Enter Job Description", height=200)
    min_score = st.slider("Minimum ATS Score", 0, 100, 70)
    
    if st.button("Find Matching Candidates"):
        matches = db.find_matches(job_desc, min_score)
        
        if matches:
            df = pd.DataFrame(matches)
            st.dataframe(df)
        else:
            st.info("No matching candidates found.")

def analytics_page(db):
    st.header("📈 Analytics Dashboard")
    
    stats = db.get_analytics()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Resumes", stats['total_resumes'])
    with col2:
        st.metric("Average Score", f"{stats['avg_score']:.1f}%")
    with col3:
        st.metric("Top Score", f"{stats['max_score']:.1f}%")
    
    # Score distribution
    scores = db.get_score_distribution()
    if scores:
        fig = px.histogram(scores, title="ATS Score Distribution")
        st.plotly_chart(fig, use_container_width=True)

def database_page(db):
    st.header("🗄️ Resume Database")
    
    resumes = db.get_all_resumes()
    if resumes:
        df = pd.DataFrame(resumes)
        st.dataframe(df)
        
        if st.button("Clear Database"):
            db.clear_database()
            st.success("Database cleared!")
    else:
        st.info("No resumes in database.")

if __name__ == "__main__":
    main()