 <div align="center">

# 🚀 CareerForge AI
### Dynamic Portfolio & Resume Generator

**Build your professional identity, create an impressive resume, showcase your projects, analyze job opportunities, and manage your career journey — all in one place.**

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://dynamic-portfolio-resume-generator-t7hhfx3eyspgz5iy5vxfrk.streamlit.app/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Authentication](https://img.shields.io/badge/Authentication-Enabled-success)](#-authentication--privacy)
[![Deployment](https://img.shields.io/badge/Deployment-Live-success)](https://dynamic-portfolio-resume-generator-t7hhfx3eyspgz5iy5vxfrk.streamlit.app/)

</div>

---

## 📌 Table of Contents

1. [About the Project](#-about-the-project)
2. [Live Demo](#-live-demo)
3. [Why I Built This](#-why-i-built-this)
4. [Features](#-features)
5. [How It Works](#-how-it-works)
6. [Authentication & Privacy](#-authentication--privacy)
7. [Tech Stack](#-tech-stack)
8. [Project Structure](#-project-structure)
9. [Run the Project on Your Computer](#-run-the-project-on-your-computer)
10. [How to Use the App](#-how-to-use-the-app)
11. [Testing](#-testing)
12. [Deploy Online for Free](#-deploy-online-for-free)
13. [Common Problems and Fixes](#-common-problems-and-fixes)
14. [Frequently Asked Questions](#-frequently-asked-questions)
15. [Future Plans](#-future-plans)
16. [Contributing](#-contributing)
17. [Author](#-author)
18. [License](#-license)

---

## 📖 About the Project

**CareerForge AI** is a modern career development web application built using **Python and Streamlit**.

It is designed to simplify the process of building a professional identity and managing a job search.

Enter your professional information once, including your name, education, skills, experience, and projects. CareerForge AI provides several tools to help you use that information effectively.

With CareerForge AI, you can:

- Generate a professional **PDF resume**.
- Create and download a personal **HTML portfolio website**.
- Analyze job descriptions and discover your **job match score**.
- Identify matching and missing skills or keywords.
- Track job applications, interviews, offers, and follow-ups.
- View your career progress through an interactive dashboard.
- Manage your profile and privacy settings.

The application also includes user authentication and user-specific profile and application management.

**CareerForge AI brings essential career tools together in one simple platform.**

---

## 🔗 Live Demo

**👉 [Click here to open CareerForge AI](https://dynamic-portfolio-resume-generator-t7hhfx3eyspgz5iy5vxfrk.streamlit.app/)**

- No installation is required.
- Works in modern web browsers on desktop and mobile.
- Hosted on Streamlit Community Cloud.
- Create an account to access the application's user-specific features.

**Note:** Streamlit Community Cloud may temporarily put an inactive application to sleep. If a wake-up screen appears, click the button and wait for the application to start.

---

## 🎯 Why I Built This

When applying for jobs, students and job seekers often face several problems:

- Creating a professional resume takes time.
- Maintaining different resumes for different job roles can be difficult.
- Building a personal portfolio website often requires coding knowledge.
- It is not always clear which skills a job description requires.
- Missing keywords can make it harder to tailor a resume.
- Managing multiple job applications manually becomes confusing.
- Remembering interview dates and follow-up dates is difficult.

I wanted to create a single platform that makes these tasks easier.

**CareerForge AI aims to make career preparation more organized, accessible, and efficient.**

---

## ✨ Features

### 1. 📊 Interactive Career Dashboard

A central dashboard that provides an overview of your job search.

- Total job applications.
- Active applications.
- Interview progress.
- Job offers.
- Application status breakdown.
- Recent applications.
- Upcoming follow-ups.
- Overdue follow-ups.

### 2. 👤 Profile Management

Maintain your professional information in one place.

- Personal information.
- Contact details.
- Professional summary.
- Technical and professional skills.
- Work experience.
- Educational qualifications.
- Projects and achievements.

Your profile can be used by the resume generator, portfolio generator, and job matching tools.

### 3. 📄 Professional Resume Generator

Create a professional resume using your saved profile.

- Generate a downloadable PDF resume.
- Include personal and contact information.
- Showcase professional skills.
- Add education and experience.
- Include project information.
- Organize your career details in a structured format.

The generated resume is designed to use a clear, readable layout. However, ATS compatibility can vary between recruitment systems.

### 4. 🌐 Personal Portfolio Generator

Turn your professional profile into a personal portfolio website.

- Generate a downloadable HTML portfolio.
- Showcase your professional introduction.
- Display your skills and experience.
- Highlight education and projects.
- Include contact and professional links.
- Create a personal online presence without manually writing HTML.

The generated HTML file can be hosted using services such as GitHub Pages or Netlify.

### 5. 🤖 Job Match Analysis

Understand how closely your profile matches a job description.

Paste a job description and analyze it against your profile.

The tool provides:

- Job match percentage.
- Matching keywords.
- Missing keywords.
- Suggestions for improving your profile and application.

This helps you identify relevant skills and tailor your application before applying.

**Note:** The match percentage is an indicative keyword-based analysis, not a guarantee of ATS selection or job eligibility.

### 6. 📌 Job Application Tracker

Manage your job search in one organized place.

You can:

- Add new job applications.
- Record company names.
- Save job titles and job links.
- Record application dates.
- Set follow-up dates.
- Add personal notes.
- Update application statuses.
- Edit existing records.
- Delete applications when needed.

Track your progress through statuses such as Applied, Interview, Offer, and Rejected, depending on the statuses supported by the application.

### 7. 🔐 Authentication & Privacy

CareerForge AI includes account authentication and user-specific data management.

- Create an account.
- Log in securely.
- Password hashing using PBKDF2-HMAC-SHA256.
- Store profiles separately for individual users.
- Manage personal application records.
- Access account and privacy settings.
- Download available personal data.
- Access available data deletion options.

### 8. ⚙️ Settings & Privacy

A dedicated section for managing your account and personal information.

- View account information.
- Review privacy-related information.
- Manage profile data.
- Download available data.
- Delete supported profile and application records.
- Log out securely.

### 9. 🎨 Modern SaaS-Style Interface

CareerForge AI includes a modern and interactive user interface.

- Clean dashboard layout.
- Modern navigation sidebar.
- Organized content sections.
- Interactive forms and controls.
- Responsive styling.
- Consistent visual design across application pages.

---

## ⚙️ How It Works

Here is the basic workflow:

```text
             Open CareerForge AI
                      |
                      ▼
             Create Account / Login
                      |
                      ▼
               Career Dashboard
                      |
                      ▼
             Complete Your Profile
                      |
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
     Resume       Portfolio     Job Match
    Generator     Generator     Analysis
         │            │            │
         ▼            ▼            ▼
      PDF File     HTML File   Match Results
         │            │            │
         └────────────┼────────────┘
                      |
                      ▼
             Application Tracker
                      |
                      ▼
            Track Career Progress
                      |
                      ▼
              Dashboard Updates
```

Each major feature is organized into separate Python modules inside the `src` folder, making the project easier to maintain and extend.

---

## 🔐 Authentication & Privacy

CareerForge AI provides account authentication and user-specific data handling.

### What it does

- Allows users to register and log in.
- Uses salted PBKDF2-HMAC-SHA256 password hashing.
- Associates profile information with individual user accounts.
- Keeps application records associated with their respective users.
- Provides account and privacy management options.
- Includes optional Supabase-backed submission storage for administrative review.

### Configuration

If your deployment uses Supabase, create:

`.streamlit/secrets.toml`

Add your private configuration:

```toml
[database]
url = "YOUR_SUPABASE_PROJECT_URL"
service_role_key = "YOUR_SUPABASE_SECRET_KEY"

[admin]
password = "YOUR_PRIVATE_ADMIN_PASSWORD"
```

### On Streamlit Community Cloud

1. Open your Streamlit application dashboard.
2. Go to **Settings**.
3. Open **Secrets**.
4. Add the required configuration.
5. Save your changes.

### Important Security Tips

- Never upload `secrets.toml` to GitHub.
- Never expose your Supabase service-role key.
- Use strong passwords.
- Do not share private credentials.
- Keep your database credentials secure.

**Storage note:** SQLite data stored on Streamlit Community Cloud may not survive restarts or redeployments. Use persistent database storage for important production data.

---

## 🛠️ Tech Stack

| Area | Technology |
|---|---|
| Programming Language | Python 3.10+ |
| Web Framework | Streamlit |
| Frontend Styling | HTML and CSS |
| Database | SQLite |
| Optional Cloud Storage | Supabase |
| Resume Generation | PDF generation |
| Portfolio Generation | HTML generation |
| Job Analysis | Python keyword matching |
| Authentication | PBKDF2-HMAC-SHA256 |
| Version Control | Git and GitHub |
| Deployment | Streamlit Community Cloud |

---

## 🗂️ Project Structure

```text
CareerForge-AI/
│
├── app.py                       # Main Streamlit application
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
│
├── .gitignore                   # Git ignored files
│
├── .streamlit/
│   └── secrets.toml             # Private configuration
│
└── src/
    ├── __init__.py              # Python package initializer
    │
    ├── auth.py                  # Registration and login logic
    ├── auth_ui.py               # Authentication interface
    ├── user_data.py             # User-specific data management
    │
    ├── resume_generator.py      # PDF resume generation
    ├── portfolio_generator.py   # HTML portfolio generation
    │
    ├── job_matcher.py           # Job description analysis
    ├── application_tracker.py   # Job application management
    ├── validation.py            # Profile and input validation
    ├── dashboard.py             # Dashboard data and statistics
    │
    ├── privacy_settings.py      # Privacy and database settings
    └── privacy_store.py         # Optional submission storage
```

---

## 💻 Run the Project on Your Computer

### What You Need First

- Python 3.10 or newer.
- pip package manager.
- Git installed on your computer.
- A code editor such as VS Code.

### Step 1: Download the Project

```bash
git clone https://github.com/anujkumardubey152-bot/Dynamic_Portfolio_Resume_Generator.git

cd Dynamic_Portfolio_Resume_Generator
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Secrets

If you are using Supabase, create:

```text
.streamlit/secrets.toml
```

Add the required private configuration as explained in the Authentication & Privacy section.

Do not commit this file to GitHub.

### Step 5: Start the Application

```bash
streamlit run app.py
```

Your browser should open the application at:

```text
http://localhost:8501
```

If it does not open automatically, copy the address into your browser.

---

## 📱 How to Use the App

1. Open [CareerForge AI](https://dynamic-portfolio-resume-generator-t7hhfx3eyspgz5iy5vxfrk.streamlit.app/).
2. Create a new account or log in.
3. Open the Dashboard to view your career overview.
4. Go to Profile & Resume.
5. Enter your personal and professional details.
6. Save your profile.
7. Generate and download your PDF resume.
8. Open Portfolio to generate your HTML portfolio.
9. Visit Job Match and paste a job description.
10. Review your match percentage and missing keywords.
11. Open Application Tracker.
12. Add jobs you have applied for and update their statuses.
13. Return to Dashboard to monitor your progress.
14. Use Settings & Privacy to manage your account and available data options.
15. Log out when you finish.

---

## 🧪 Testing

The application includes separate modules for its major features.

You can perform manual testing by checking:

| Feature | What to Test |
|---|---|
| Authentication | Register, log in, and log out |
| Profile | Save and reload profile information |
| Resume | Generate and download a PDF |
| Portfolio | Generate and download HTML |
| Job Match | Analyze a sample job description |
| Tracker | Add, edit, update, and delete applications |
| Dashboard | Check application statistics |
| Privacy | Test available data management options |

If automated tests are included in your repository, run them using:

```bash
python -m pytest
```

---

## 🌐 Deploy Online for Free

CareerForge AI is deployed using **Streamlit Community Cloud**.

You can also deploy your own version.

### Deployment Steps

1. Push your project to a GitHub repository.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in with your GitHub account.
4. Click **Create App**.
5. Select your repository.
6. Choose the `main` branch.
7. Set the main file path to `app.py`.
8. Open Advanced Settings and configure the required secrets.
9. Click **Deploy**.

After deployment, Streamlit will provide a public application URL.

**Live Project:** https://dynamic-portfolio-resume-generator-t7hhfx3eyspgz5iy5vxfrk.streamlit.app/

---

## 🩺 Common Problems and Fixes

### "Streamlit is not recognized" or "command not found"

Streamlit may not be installed, or your virtual environment may not be activated.

Run:

```bash
pip install -r requirements.txt
```

### The app says a Python module is missing

Install the dependencies again:

```bash
pip install -r requirements.txt
```

Also check that you are running the command from the project directory.

### Login or registration is not working

Check the application logs and verify that the database is configured correctly.

### Supabase configuration error

Check that the required secrets are correctly configured in `.streamlit/secrets.toml` or the Streamlit Cloud Secrets settings.

### PDF or HTML file is not downloading

Check that your profile contains the required information and that all validation checks have passed.

### The live application is slow to open

Streamlit Community Cloud may put inactive applications to sleep. Wait for the application to wake up.

### Saved application data disappears after redeployment

SQLite files on temporary cloud storage may not be persistent. Use a persistent cloud database for important information.

---

## ❓ Frequently Asked Questions

**Is CareerForge AI free to use?**

The live application is publicly accessible. Hosting, database, and third-party service availability may be subject to their respective limits and policies.

**Do I need programming knowledge to use it?**

No. You can use the application through its interactive interface. Programming knowledge is only needed if you want to modify the source code.

**What is an ATS-friendly resume?**

ATS stands for Applicant Tracking System. Companies use these systems to process and organize resumes. A clear, structured resume can make its content easier for such systems to read, although no format guarantees successful parsing.

**Can I host my generated portfolio online?**

Yes. The generated HTML portfolio can be hosted on services such as GitHub Pages, Netlify, or another web hosting provider.

**Does Job Match guarantee that I will get selected?**

No. It provides an indicative comparison of profile keywords and job description requirements. Hiring decisions depend on many other factors.

**Can different users manage their own profiles?**

The application includes user-specific profile and application data management.

**Is my data permanently stored?**

Storage persistence depends on the database configuration. Local SQLite storage on Streamlit Community Cloud should not be treated as permanent.

**Can I customize the resume or portfolio design?**

Yes. Developers can modify `src/resume_generator.py` and `src/portfolio_generator.py` to customize the generated documents.

---

## 🗺️ Future Plans

Some ideas for future development:

- [ ] Multiple professional resume templates.
- [ ] Advanced ATS resume analysis.
- [ ] AI-powered resume improvement suggestions.
- [ ] AI cover letter generator.
- [ ] Advanced job recommendations.
- [ ] More portfolio customization options.
- [ ] Project showcase with GitHub and live demo links.
- [ ] Email reminders for job follow-ups.
- [ ] Export application records to CSV or Excel.
- [ ] Persistent cloud database integration.
- [ ] Advanced career analytics.
- [ ] Additional profile and account customization.

---

## 🤝 Contributing

Ideas, suggestions, and improvements are welcome!

If you want to contribute:

1. Fork this repository.
2. Create a new branch:

```bash
git checkout -b my-new-feature
```

3. Make your changes.
4. Commit your improvements:

```bash
git commit -m "Add new feature"
```

5. Push your branch:

```bash
git push origin my-new-feature
```

6. Open a Pull Request.

---

## 👨‍💻 Author

**Anuj Kumar Dubey**

B.Tech CSE, IERT Prayagraj | AI/ML Developer

I am passionate about Python development, artificial intelligence, machine learning, and building practical software solutions.

### Connect With Me

[![GitHub](https://img.shields.io/badge/GitHub-anujkumardubey152--bot-181717?style=for-the-badge&logo=github)](https://github.com/anujkumardubey152-bot)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Anuj_Kumar_Dubey-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/anuj-kumar-dubey-58043b377/)

### Try My Project

[![Live App](https://img.shields.io/badge/🚀_Open_CareerForge_AI-Live_Demo-success?style=for-the-badge)](https://dynamic-portfolio-resume-generator-t7hhfx3eyspgz5iy5vxfrk.streamlit.app/)

If you like this project, please give it a ⭐ on GitHub. It really helps!

---

## 📜 License

This project is licensed under the MIT License.

You are free to use, modify, and distribute the project according to the terms of the MIT License.

See the `LICENSE` file for details.

---

<div align="center">

### 🚀 CareerForge AI

**Build Your Profile. Showcase Your Skills. Shape Your Future.**

Made with ❤️ by **Anuj Kumar Dubey**

[Live Demo](https://dynamic-portfolio-resume-generator-t7hhfx3eyspgz5iy5vxfrk.streamlit.app/) · [GitHub](https://github.com/anujkumardubey152-bot) · [LinkedIn](https://www.linkedin.com/in/anuj-kumar-dubey-58043b377/)

</div>
