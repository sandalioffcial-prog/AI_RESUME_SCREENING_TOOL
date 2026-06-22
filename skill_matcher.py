# Import required libraries

# Converts text into numerical vectors using TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer

# Calculates similarity between two vectors
from sklearn.metrics.pairwise import cosine_similarity


def extract_skills(text, skills_list):
    """
    Extract skills from the resume text.

    Parameters:
        text (str): Resume text
        skills_list (list): Master list of skills to search for

    Returns:
        list: Skills found in the resume
    """

    # Convert text to lowercase for case-insensitive matching
    text = text.lower()

    # Store detected skills
    found_skills = []

    # Check each skill in the master skill list
    for skill in skills_list:

        # If the skill exists in the resume text
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def calculate_skill_match(resume_skills, jd_skills):
    """
    Compare resume skills with job description skills.

    Parameters:
        resume_skills (list): Skills found in resume
        jd_skills (list): Skills required in job description

    Returns:
        score (float): Skill match percentage
        matched_skills (list): Common skills
        missing_skills (list): Required skills not found
    """

    # Prevent division by zero
    if len(jd_skills) == 0:
        return 0, [], []

    # Skills present in both resume and job description
    matched_skills = list(
        set(resume_skills).intersection(set(jd_skills))
    )

    # Skills required but missing from resume
    missing_skills = list(
        set(jd_skills).difference(set(resume_skills))
    )

    # Calculate matching percentage
    score = (len(matched_skills) / len(jd_skills)) * 100

    return score, matched_skills, missing_skills


def calculate_tfidf_similarity(resume_text, jd_text):
    """
    Calculate text similarity between
    resume and job description using TF-IDF.

    Parameters:
        resume_text (str): Resume content
        jd_text (str): Job description content

    Returns:
        float: Similarity percentage
    """

    # Store both documents together
    documents = [resume_text, jd_text]

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Convert documents into numerical vectors
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Calculate cosine similarity between the two vectors
    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    # Convert decimal value to percentage
    return similarity * 100


def calculate_final_score(tfidf_score, skill_score):
    """
    Calculate the final resume score.

    Weight Distribution:
    - 70% TF-IDF Similarity
    - 30% Skill Match Score

    Parameters:
        tfidf_score (float)
        skill_score (float)

    Returns:
        float: Final score rounded to 2 decimal places
    """

    return round(
        (0.7 * tfidf_score) +
        (0.3 * skill_score),
        2
    )


def get_match_category(score):
    """
    Convert numerical score into a category.

    Parameters:
        score (float)

    Returns:
        str: Match category
    """

    # Excellent candidate match
    if score >= 80:
        return "Excellent Match"

    # Good candidate match
    elif score >= 60:
        return "Good Match"

    # Average candidate match
    elif score >= 40:
        return "Average Match"

    # Weak candidate match
    return "Poor Match"
