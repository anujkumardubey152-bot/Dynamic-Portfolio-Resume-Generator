
# 🚀 CareerForge AI
### Your Career. Your Story. Your Future.

<p align="center">
  <a href="https://dynamic-portfolio-resume-generator.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀_Live_Demo-Launch_App-success?style=for-the-badge" alt="Live Demo">
  </a>
  <a href="https://github.com/anujkumardubey152-bot">
    <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  <a href="https://www.linkedin.com/in/anuj-kumar-dubey-58043b377/">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin" alt="LinkedIn">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Framework-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/AI-Powered-8A2BE2?style=for-the-badge" alt="AI Powered">
  <img src="https://img.shields.io/badge/Status-Live-success?style=for-the-badge" alt="Live">
</p>

---

## 🌟 About CareerForge AI

**CareerForge AI** is an interactive career development platform designed to help job seekers build professional resumes, create personal portfolios, analyze job descriptions, and manage job applications — all in one place.

Whether you're a student, fresher, graduate, or experienced professional, CareerForge AI helps you build your professional identity and organize your career journey.

🎯 **One platform. Multiple career tools. A smarter job search.**

## 🌐 Live Application

<p align="center">
  <a href="https://dynamic-portfolio-resume-generator.streamlit.app/">
    <img src="https://img.shields.io/badge/OPEN_CAREERFORGE_AI-Click_Here-2563EB?style=for-the-badge&logo=streamlit&logoColor=white" alt="Open CareerForge AI">
  </a>
</p>

🔗 **Live Demo:** https://dynamic-portfolio-resume-generator.streamlit.app/

Try the application and explore its career-building features!

---

## ✨ Features

### 📊 1. Interactive Career Dashboard
- View job application statistics.
- Monitor active applications, interviews, and offers.
- Track upcoming and overdue follow-ups.
- Get an overview of your career progress.

### 📄 2. Professional Resume Generator
- Create a structured professional resume.
- Add personal information, professional summary, skills, education, and experience.
- Generate downloadable PDF resumes.
- Keep your professional information organized.

### 🌐 3. Personal Portfolio Generator
- Generate a professional portfolio website.
- Showcase skills, projects, education, and experience.
- Include professional links and contact information.
- Download your portfolio as an HTML file.

### 🤖 4. Job Match Analysis
- Analyze job descriptions against your profile.
- Identify matching skills and keywords.
- Discover missing keywords.
- Get suggestions to improve your job applications.

### 📌 5. Job Application Tracker
- Add and manage job applications.
- Track application statuses.
- Record company names and job titles.
- Set follow-up dates and add notes.
- Update or delete application records.

### 🔐 6. Authentication & Privacy
- User registration and login.
- Secure password hashing.
- User-specific profile and application data.
- Privacy and data management options.

---

## 🖥️ Application Pages

| Page | Purpose |
|---|---|
| Dashboard | Career statistics and progress |
| Profile & Resume | Manage profile and generate resumes |
| Portfolio | Create and download portfolios |
| Job Match | Analyze job descriptions |
| Application Tracker | Manage job applications |
| Settings & Privacy | Manage account and privacy |

---

## 🛠️ Technology Stack

| Technology | Usage |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| SQLite | Local data storage |
| Supabase | Optional submission storage |
| HTML | Portfolio generation |
| CSS | Frontend styling |
| AI / NLP logic | Job description and keyword analysis |
| Git & GitHub | Version control |
| Streamlit Community Cloud | Deployment |

---

## 📁 Project Structure

```text
CareerForge-AI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── .streamlit/
│   └── secrets.toml
│
└── src/
    ├── __init__.py
    ├── auth.py
    ├── auth_ui.py
    ├── user_data.py
    ├── resume_generator.py
    ├── portfolio_generator.py
    ├── job_matcher.py
    ├── application_tracker.py
    ├── validation.py
    ├── dashboard.py
    ├── privacy_settings.py
    └── privacy_store.py
```

---

## ⚙️ Installation & Setup

Want to run CareerForge AI on your local machine? Follow these steps.

### 1. Clone the Repository

```bash
git clone https://github.com/anujkumardubey152-bot/YOUR-REPOSITORY.git
```

Replace `YOUR-REPOSITORY` with your actual repository name.

### 2. Navigate to the Project Folder

```bash
cd YOUR-REPOSITORY
```

### 3. Create a Virtual Environment

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

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Secrets (If Using Supabase)

Create:

```text
.streamlit/secrets.toml
```

Add your private configuration:

```toml
[database]
url = "YOUR_SUPABASE_PROJECT_URL"
service_role_key = "YOUR_SUPABASE_SECRET_KEY"

[admin]
password = "YOUR_PRIVATE_ADMIN_PASSWORD"
```

⚠️ Never upload your private `secrets.toml` file or credentials to GitHub.

### 6. Run the Application

```bash
streamlit run app.py
```

Open your browser at:

```text
http://localhost:8501
```

---

## ☁️ Deployment

CareerForge AI is deployed using **Streamlit Community Cloud**.

To deploy your own version:

1. Push your project to GitHub.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in with GitHub.
4. Select **Create app**.
5. Choose your repository and branch.
6. Set the main file path to `app.py`.
7. Configure required secrets in the app settings.
8. Click **Deploy**.

---

## 🔒 Security & Privacy

CareerForge AI includes authentication and privacy-related functionality.

- Passwords use salted PBKDF2-HMAC-SHA256 hashing.
- User profiles and applications are associated with individual accounts.
- Administrative credentials should remain private.
- Supabase service-role keys must never be exposed publicly.
- Users can access available privacy and data management options.

**Note:** SQLite storage on Streamlit Community Cloud may not persist across restarts or redeployments. A persistent database is recommended for production use.

---

## 🎯 Project Objectives

- Simplify professional resume creation.
- Help users establish an online professional identity.
- Improve understanding of job requirements.
- Make job application tracking easier.
- Encourage organized career development.
- Provide useful career tools in one platform.

---

## 🚀 Future Enhancements

- [ ] AI-powered resume improvement.
- [ ] ATS-friendly resume scoring.
- [ ] Multiple resume templates.
- [ ] Advanced portfolio customization.
- [ ] AI cover letter generator.
- [ ] Personalized job recommendations.
- [ ] Email reminders for follow-ups.
- [ ] Persistent cloud database integration.
- [ ] Advanced career analytics.

---

## 👨‍💻 About the Developer

### Anuj Kumar Dubey

Aspiring Software Developer | Python Developer | Technology Enthusiast

I developed **CareerForge AI** to bring essential career-building tools together in one accessible platform.

I'm passionate about Python development, web applications, and building practical technology solutions.

<p align="left">
  <a href="https://github.com/anujkumardubey152-bot">
    <img src="https://img.shields.io/badge/GitHub-Follow_Me-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  <a href="https://www.linkedin.com/in/anuj-kumar-dubey-58043b377/">
    <img src="https://img.shields.io/badge/LinkedIn-Connect_With_Me-0A66C2?style=for-the-badge&logo=linkedin" alt="LinkedIn">
  </a>
</p>

---

## 🤝 Contributions

Suggestions, feedback, and contributions are welcome!

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Commit your improvements.
5. Submit a Pull Request.

---

## 📜 License

This project is currently shared for educational and portfolio purposes.

Add a `LICENSE` file if you decide to distribute it under a specific open-source license.

---

## ⭐ Show Your Support

If you like CareerForge AI:

- ⭐ Star the GitHub repository.
- 🚀 Try the live application.
- 💬 Share your feedback.
- 🤝 Connect with me on LinkedIn.

---

<p align="center">
  <b>CareerForge AI</b>
  <br>
  Build Your Profile. Showcase Your Skills. Shape Your Future. 🚀
  <br><br>
  Made with ❤️ by <a href="https://github.com/anujkumardubey152-bot">Anuj Kumar Dubey</a>
</p>
