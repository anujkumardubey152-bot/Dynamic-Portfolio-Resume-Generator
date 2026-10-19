<div align="center">

# 📄 Dynamic Portfolio & Resume Generator

**Build an ATS-friendly resume and a shareable portfolio from one profile, match it to job descriptions, and track every application.**

[

![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-FF4B4B?style=for-the-badge)

](https://dynamic-portfolio-resume-generator-iadgynjbtxlywu23bkczti.streamlit.app/)



![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)




![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)




![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)




![License](https://img.shields.io/badge/License-MIT-green)



</div>




---




## 🔗 Live Demo

**👉 [Open the app](https://dynamic-portfolio-resume-generator-iadgynjbtxlywu23bkczti.streamlit.app/)**

No installation needed. Fill in the profile form, then download your resume and portfolio. The app is hosted on Streamlit Community Cloud and may take a few seconds to wake up if it has been idle.




---




## 🎯 Problem It Solves

Job seekers rewrite the same details for every resume, portfolio, and application, and many resumes are filtered out by ATS software before a human reads them. This app keeps everything in one place:

1. Enter your details **once**
2. Generate an **ATS-friendly PDF resume** and an **HTML portfolio**
3. Check how well you match a **job description**
4. **Track applications** from submission to offer




---




## ✨ Features

| Feature | Description |
|---|---|
| **Profile Form** | Personal info, education, skills, experience, and projects in one place |
| **PDF Resume** | Clean, single-column, ATS-friendly layout |
| **HTML Portfolio** | Standalone page you can download and host anywhere |
| **Job Matcher** | Paste a job description to get a keyword match score and see missing skills |
| **Application Tracker** | SQLite-backed add, edit, delete, and status tracking |
| **Dashboard** | Overview of your application pipeline |
| **Input Validation** | Checks emails, phone numbers, and URLs before generating documents |
| **Privacy Settings** | Choose which details appear in your resume and portfolio |




---




## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **UI:** Streamlit
- **Database:** SQLite
- **Documents:** PDF generation and HTML templating
- **Testing:** pytest
- **Deployment:** Streamlit Community Cloud




---




## 🚀 Run Locally

```bash
git clone https://github.com/anujkumardubey152-bot/Dynamic_Portfolio_Resume_Generator.git
cd Dynamic_Portfolio_Resume_Generator

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in your browser.




---




## 📖 How to Use

1. **Fill in your profile** with your details, skills, and projects.
2. **Set privacy preferences** to choose what is shown publicly.
3. **Generate** your PDF resume and HTML portfolio, then download them.
4. **Paste a job description** into the Job Matcher to see your match score.
5. **Log applications** in the Tracker and monitor progress on the Dashboard.




---




## 🗂️ Project Structure

```
Dynamic_Portfolio_Resume_Generator/
├── app.py                      # Streamlit entry point
├── requirements.txt            # Dependencies
├── test_generators.py          # Tests for generators
├── README.md
├── .gitignore
└── src/
    ├── __init__.py
    ├── application_tracker.py  # SQLite CRUD for applications
    ├── dashboard.py            # Pipeline stats and overview
    ├── job_matcher.py          # Keyword and skill matching
    ├── portfolio_generator.py  # HTML portfolio builder
    ├── privacy_settings.py     # Control shared data
    ├── resume_generator.py     # ATS-friendly PDF builder
    └── validation.py           # Input validation helpers
```




---




## 🧪 Testing

```bash
python -m pytest test_generators.py
```




---




## 🗺️ Roadmap

- [ ] Multiple resume templates
- [ ] Semantic job matching using embeddings
- [ ] Cover letter generator
- [ ] Export tracker data to CSV




---




## 👨‍💻 Author

**Anuj Kumar Dubey**
B.Tech CSE, IERT Prayagraj | AI/ML Developer

[

![GitHub](https://img.shields.io/badge/GitHub-anujkumardubey152--bot-181717?logo=github)

](https://github.com/anujkumardubey152-bot)




---




