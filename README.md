<div align="center">

# 📄 Dynamic Portfolio & Resume Generator

**A simple web app that helps you make a professional resume, create a portfolio website, check how well you fit a job, and keep track of all your job applications. It also has a secure admin login.**

[

![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-FF4B4B?style=for-the-badge)

](https://dynamic-portfolio-resume-generator-iadgynjbtxlywu23bkczti.streamlit.app/)



![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)




![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)




![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)




![Auth](https://img.shields.io/badge/Admin-Authorization-success)




![License](https://img.shields.io/badge/License-MIT-green)



</div>




---




## 📌 Table of Contents

1. [About the Project](#-about-the-project)
2. [Live Demo](#-live-demo)
3. [Why I Built This](#-why-i-built-this)
4. [Features](#-features)
5. [How It Works](#-how-it-works)
6. [Admin Authorization](#-admin-authorization)
7. [Tech Stack](#-tech-stack)
8. [Project Structure](#-project-structure)
9. [Run the Project on Your Computer](#-run-the-project-on-your-computer)
10. [How to Use the App](#-how-to-use-the-app)
11. [Testing](#-testing)
12. [Deploy Online for Free](#-deploy-online-for-free)
13. [Common Problems and Fixes](#-common-problems-and-fixes)
14. [Frequently Asked Questions](#-frequently-asked-questions)
15. [Future Plans](#-future-plans)
16. [Author](#-author)
17. [License](#-license)




---




## 📖 About the Project

**Dynamic Portfolio & Resume Generator** is a web application built with **Python** and **Streamlit**.

You type your details one time, such as your name, education, skills, projects, and experience. The app then does the rest for you:

- It creates a clean **PDF resume** that company software (called ATS) can read easily.
- It creates a **portfolio website** (an HTML file) that you can download and put online.
- It compares your skills with a **job description** and tells you how well you match.
- It lets you **track every job you apply for** in one place.
- It keeps important admin pages safe with a **login system**.

You do not need to know coding to use it. Just open the link, fill in the form, and download your files.




---




## 🔗 Live Demo

**👉 [Click here to open the app](https://dynamic-portfolio-resume-generator-iadgynjbtxlywu23bkczti.streamlit.app/)**

- No installation is needed.
- It works in any browser, on phone or computer.
- The app is hosted on **Streamlit Community Cloud** (free hosting). If nobody has used it for a while, it goes to sleep. If you see a "wake up" button, click it and wait a few seconds.




---




## 🎯 Why I Built This

When you apply for jobs, a few things are annoying:

- You have to **write the same details again and again** in different resumes.
- Many companies use **ATS software** (Applicant Tracking System). It scans your resume first. If your resume has a fancy design or confusing layout, the software may not read it correctly, and a human may never see it.
- It is hard to know **which skills a job wants** and which ones you are missing.
- After applying to many companies, it is easy to **forget where you applied** and what happened next.

This project solves all of these problems in one app.




---




## ✨ Features

### 1. Profile Form
Fill in your personal details, education, skills, work experience, and projects in one simple form. You only need to do this once.

### 2. ATS-Friendly PDF Resume
The app creates a clean, single-column PDF resume. It has no confusing tables or heavy graphics, so ATS software can read it properly.

### 3. HTML Portfolio
The app builds a portfolio web page from your profile. You can download it and host it anywhere, for example on GitHub Pages.

### 4. Job Matcher
Paste any job description. The app compares it with your skills and shows:
- Your match score
- Keywords that you already have
- Keywords that you are missing

This helps you improve your resume before you apply.

### 5. Application Tracker
Keep a record of every job you apply for. You can:
- Add a new application
- Edit the details
- Delete an application
- Update the status (Applied, Interview, Offer, Rejected, and so on)

Your data is saved in a **SQLite** database.

### 6. Dashboard
See a quick summary of all your applications. It helps you understand how your job search is going.

### 7. Input Validation
The app checks your email, phone number, and links before creating any document. This avoids silly mistakes like a wrong email in your resume.

### 8. Privacy Settings
You decide which details are shown in your resume and portfolio. For example, you can hide your phone number from a public portfolio.

### 9. Admin Authorization
Some pages are only for the admin. A visitor must log in with the correct admin username and password to open them. Normal visitors can still use the public tools.




---




## ⚙️ How It Works

Here is the simple flow of the app:

```
You open the app
      │
      ▼
Fill in the Profile Form  ───►  Validation checks your input
      │
      ▼
Choose what to show in Privacy Settings
      │
      ├──►  Resume Generator   ───►  Download PDF resume
      │
      ├──►  Portfolio Generator ──►  Download HTML portfolio
      │
      ├──►  Job Matcher        ───►  See match score and missing skills
      │
      └──►  Application Tracker ──►  Saved in SQLite database
                                          │
                                          ▼
                                      Dashboard

Admin pages  ───►  Locked until the admin logs in
```

Each part of the app lives in its own Python file inside the `src` folder. This keeps the code clean and easy to understand.




---




## 🔐 Admin Authorization

Admin authorization means **only the right person can open the protected pages**.

### What it does

- Asks for an admin username and password before opening admin-only pages
- Keeps passwords **out of the code**, so they are not visible on GitHub
- Keeps the admin logged in during the session and lets them log out
- Stops normal visitors from seeing or changing admin-only data

### How to set up admin credentials

**On your own computer**

Create a file at `.streamlit/secrets.toml` and add:

```toml
ADMIN_USERNAME = "your_admin_username"
ADMIN_PASSWORD = "your_strong_password"
```

**On Streamlit Community Cloud**

1. Open your app dashboard.
2. Click **Settings**, then **Secrets**.
3. Paste the same two lines and save.

### Safety tips

- ⚠️ Never upload `secrets.toml` to GitHub. Add `.streamlit/secrets.toml` to your `.gitignore` file.
- Use a long and strong password. Do not use simple ones like `admin123`.
- Do not share your admin login with anyone you do not trust.
- Change your password if you think someone else has seen it.




---




## 🛠️ Tech Stack

| Area | Tool Used |
|---|---|
| Programming Language | Python 3.10+ |
| Web Framework | Streamlit |
| Database | SQLite |
| Resume Output | PDF generation |
| Portfolio Output | HTML templating |
| Security | Admin authorization with secrets |
| Testing | pytest |
| Hosting | Streamlit Community Cloud |




---




## 🗂️ Project Structure

```
Dynamic_Portfolio_Resume_Generator/
├── app.py                      # Main file. Starts the Streamlit app
├── requirements.txt            # List of Python packages needed
├── test_generators.py          # Tests for resume and portfolio generators
├── README.md                   # This file
├── .gitignore                  # Files that Git should ignore
├── .streamlit/
│   └── secrets.toml            # Admin login details (never upload this)
└── src/
    ├── __init__.py             # Makes src a Python package
    ├── application_tracker.py  # Add, edit, delete job applications (SQLite)
    ├── dashboard.py            # Summary and stats of applications
    ├── job_matcher.py          # Matches your skills with a job description
    ├── portfolio_generator.py  # Builds the HTML portfolio
    ├── privacy_settings.py     # Controls what details are shown
    ├── resume_generator.p