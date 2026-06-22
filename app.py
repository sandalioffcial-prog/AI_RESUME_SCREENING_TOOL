# Import Streamlit for building the web application
import streamlit as st

# Import the master skills list
from skills import skills

# Import resume parsing functions
from resume_parser import (
    extract_resume_text,
    extract_email,
    extract_phone,
    extract_name
)

# Import AI matching functions
from skill_matcher import (
    extract_skills,
    calculate_skill_match,
    calculate_tfidf_similarity,
    calculate_final_score,
    get_match_category
)

# Import function for saving results to CSV
from save_results import save_result


# Configure the Streamlit page
st.set_page_config(
    page_title="AI Resume Screening Tool",
    page_icon="📄"
)

# Main page title
st.title("AI Resume Screening Tool")

# File uploader for PDF resumes
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# Text area where recruiter pastes the job description
job_description = st.text_area(
    "Paste Job Description"
)

# Run analysis when button is clicked
if st.button("Analyze Resume"):

    # Check if resume is uploaded
    if uploaded_file is None:
        st.error("Please upload a resume.")
        st.stop()

    # Check if job description is provided
    if not job_description.strip():
        st.error("Please enter a Job Description.")
        st.stop()

    # Extract all text from uploaded PDF resume
    resume_text = extract_resume_text(uploaded_file)

    # Extract candidate details
    name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)

    # Find skills present in the resume
    resume_skills = extract_skills(
        resume_text,
        skills
    )

    # Find skills present in the job description
    jd_skills = extract_skills(
        job_description,
        skills
    )

    # Calculate skill match score
    skill_score, matched_skills, missing_skills = (
        calculate_skill_match(
            resume_skills,
            jd_skills
        )
    )

    # Calculate TF-IDF similarity score
    tfidf_score = calculate_tfidf_similarity(
        resume_text,
        job_description
    )

    # Calculate overall weighted score
    final_score = calculate_final_score(
        tfidf_score,
        skill_score
    )

    # Convert score into a category
    category = get_match_category(
        final_score
    )

    # Display success message
    st.success("Analysis Complete")

    # Show overall score
    st.metric(
        label="Match Score",
        value=f"{final_score}%"
    )

    # Display match category
    st.subheader(category)

    st.session_state["name"] = name
    st.session_state["email"] = email
    st.session_state["phone"] = phone
    st.session_state["final_score"] = final_score
    st.session_state["category"] = category

    # Expandable section for detailed results
    with st.expander("Show Details"):

        # Candidate information section
        st.write("### Candidate Information")

        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")
        st.write(f"**Phone:** {phone}")

        # Skills detected in resume
        st.write("### Skills Found")

        if resume_skills:
            st.write(", ".join(resume_skills))
        else:
            st.write("No skills detected.")

        # Skills matching the job description
        st.write("### Matched Skills")

        if matched_skills:
            st.write(", ".join(matched_skills))
        else:
            st.write("No matched skills.")

        # Skills required but missing
        st.write("### Missing Skills")

        if missing_skills:
            st.write(", ".join(missing_skills))
        else:
            st.write("No missing skills.")

    # Save results when button is clicked
if st.button("Save Result"):

    if "final_score" not in st.session_state:
        st.error("Please analyze a resume first.")

    else:
        save_result(
            st.session_state["name"],
            st.session_state["email"],
            st.session_state["phone"],
            st.session_state["final_score"],
            st.session_state["category"]
        )

        st.success("Result saved successfully.")