# Import required libraries

# Pandas is used for creating and managing tabular data
import pandas as pd

# os is used to check whether a file already exists
import os


def save_result(name, email, phone, score, category):
    """
    Save candidate screening results to a CSV file.

    Parameters:
        name (str): Candidate's name
        email (str): Candidate's email address
        phone (str): Candidate's phone number
        score (float): Resume match score
        category (str): Match category
    """

    # Create a dictionary containing candidate information
    data = {
        "Name": [name],
        "Email": [email],
        "Phone": [phone],
        "Match Score": [score],
        "Category": [category]
    }

    # Convert dictionary into a Pandas DataFrame
    df = pd.DataFrame(data)

    # Output file name
    file_name = "saved_results.csv"

    # Check if the CSV file already exists
    if os.path.exists(file_name):

        # Append new data to existing file
        # header=False prevents column names from repeating
        # index=False removes row numbering
        df.to_csv(
            file_name,
            mode="a",
            header=False,
            index=False
        )

    else:
        # Create a new CSV file and write column headers
        df.to_csv(
            file_name,
            index=False
        )

