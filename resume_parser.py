# Import libraries
# pdfplumber is used to read text from PDF resumes
# re is used for pattern matching (emails, phone numbers, etc.)
import pdfplumber
import re


def extract_resume_text(pdf_file):
    """
    Extracts all text from a PDF resume.

    Parameters:
        pdf_file: Uploaded PDF file

    Returns:
        A string containing all text found in the PDF.
    """

    # Store extracted text
    text = ""

    # Open the PDF file
    with pdfplumber.open(pdf_file) as pdf:

        # Loop through every page in the PDF
        for page in pdf.pages:

            # Extract text from the current page
            page_text = page.extract_text()

            # Add text only if extraction was successful
            if page_text:
                text += page_text + "\n"

    # Return the complete resume text
    return text


def extract_email(text):
    """
    Finds and returns the first email address in the resume.

    Parameters:
        text (str): Resume text

    Returns:
        Email address if found, otherwise 'Not Found'
    """

    # Regular expression pattern for email addresses
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    # Find all matching email addresses
    emails = re.findall(pattern, text)

    # Return the first email found
    if emails:
        return emails[0]

    # If no email exists
    return "Not Found"


def extract_phone(text):
    """
    Finds and returns the first phone number in the resume.

    Parameters:
        text (str): Resume text

    Returns:
        Phone number if found, otherwise 'Not Found'
    """

    # Pattern for phone numbers with optional country code
    pattern = r"\+?\d[\d\s\-]{8,15}"

    # Find matching phone numbers
    phones = re.findall(pattern, text)

    # Return the first phone number found
    if phones:
        return phones[0]

    # If no phone number exists
    return "Not Found"


def extract_name(text):
    """
    Extracts the candidate's name.

    Current logic:
    Assumes the first non-empty line of the resume
    is the candidate's name.

    Parameters:
        text (str): Resume text

    Returns:
        Candidate name if found, otherwise 'Not Found'
    """

    # Split resume text into separate lines
    lines = text.split("\n")

    # Check each line one by one
    for line in lines:

        # Remove extra spaces
        line = line.strip()

        # Return the first non-empty line
        if line:
            return line

    # If no valid name is found
    return "Not Found"

