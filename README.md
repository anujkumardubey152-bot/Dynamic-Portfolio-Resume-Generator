# Dynamic Portfolio and Resume Generator

A Python and Streamlit application for creating resumes and portfolios,
matching skills against job descriptions, and tracking job applications.

## Features

- Profile form for personal and professional details
- ATS-friendly PDF resume generation
- Downloadable HTML portfolio
- Basic job-description keyword matching
- SQLite application tracker with add, edit, and delete features

## Run locally

Install dependencies:

    pip install -r requirements.txt

Start the application from the project folder:

    streamlit run app.py

## Project structure

    Dynamic_Portfolio_Resume_Generator/
    ├── app.py
    ├── requirements.txt
    ├── README.md
    ├── .gitignore
    ├── src/
    │   ├── resume_generator.py
    │   ├── portfolio_generator.py
    │   └── application_tracker.py
    └── tests/
        └── test_generators.py

## Privacy

Keep personal information and the local application database out of public
repositories. Review generated files before sharing them.
