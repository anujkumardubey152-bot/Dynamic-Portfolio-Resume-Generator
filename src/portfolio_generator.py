import html
from urllib.parse import urlsplit


def _text(value):
    """Escape text before inserting it into HTML."""
    return html.escape(str(value or "").strip(), quote=True)


def _safe_url(value):
    """Allow only safe HTTP, HTTPS, or mailto links."""
    value = str(value or "").strip()

    if not value:
        return ""

    if any(ord(char) < 32 for char in value):
        return ""

    try:
        parsed = urlsplit(value)
    except ValueError:
        return ""

    if parsed.scheme.lower() in ("http", "https"):
        if not parsed.netloc or parsed.username or parsed.password:
            return ""
        return html.escape(value, quote=True)

    if parsed.scheme.lower() == "mailto":
        if not parsed.path or "@" not in parsed.path:
            return ""
        return html.escape(value, quote=True)

    return ""


def _get_projects(profile):
    """Support both structured projects and older text-only projects."""
    structured = profile.get("project_details", []) or []

    if structured:
        projects = []

        for item in structured:
            if not isinstance(item, dict):
                continue

            title = str(item.get("title", "")).strip()

            if not title:
                continue

            technologies = item.get("technologies", []) or []

            if isinstance(technologies, str):
                technologies = [
                    tech.strip()
                    for tech in technologies.split(",")
                    if tech.strip()
                ]

            projects.append({
                "title": title,
                "description": str(
                    item.get("description", "")
                ).strip(),
                "technologies": technologies,
                "github_url": str(
                    item.get("github_url", "")
                ).strip(),
                "live_url": str(
                    item.get("live_url", "")
                ).strip(),
            })

        return projects

    # Older profiles stored each project as one string.
    return [
        {
            "title": str(project).strip(),
            "description": "",
            "technologies": [],
            "github_url": "",
            "live_url": "",
        }
        for project in profile.get("projects", [])
        if str(project).strip()
    ]


def _project_card(project):
    title = _text(project["title"])
    description = _text(project["description"])

    technology_tags = "".join(
        f'<span class="tech-tag">{_text(tech)}</span>'
        for tech in project["technologies"]
        if str(tech).strip()
    )

    github_url = _safe_url(project["github_url"])
    live_url = _safe_url(project["live_url"])

    buttons = ""

    if github_url:
        buttons += (
            f'<a class="project-button secondary" '
            f'href="{github_url}" target="_blank" '
            f'rel="noopener noreferrer">GitHub ↗</a>'
        )

    if live_url:
        buttons += (
            f'<a class="project-button primary" '
            f'href="{live_url}" target="_blank" '
            f'rel="noopener noreferrer">Live Demo ↗</a>'
        )

    description_html = (
        f'<p class="project-description">{description}</p>'
        if description else ""
    )

    technology_html = (
        f'<div class="technology-list">{technology_tags}</div>'
        if technology_tags else ""
    )

    buttons_html = (
        f'<div class="project-actions">{buttons}</div>'
        if buttons else ""
    )

    return f"""
    <article class="project-card reveal">
        <h3>{title}</h3>
        {description_html}
        {technology_html}
        {buttons_html}
    </article>
    """


def generate_portfolio_html(profile):
    """Generate a downloadable, responsive HTML portfolio."""

    name = _text(profile.get("name", "Your Name"))
    email = str(profile.get("email", "")).strip()
    phone = _text(profile.get("phone", ""))
    location = _text(profile.get("location", ""))
    summary = _text(profile.get("summary", ""))

    skills = profile.get("skills", []) or []
    experience = profile.get("experience", []) or []
    education = profile.get("education", []) or []
    projects = _get_projects(profile)

    linkedin_url = _safe_url(profile.get("linkedin", ""))
    website_url = _safe_url(profile.get("website", ""))
    email_url = _safe_url(f"mailto:{email}") if email else ""

    skill_html = "".join(
        f'<span class="skill-tag">{_text(skill)}</span>'
        for skill in skills
        if str(skill).strip()
    )

    project_html = "".join(
        _project_card(project) for project in projects
    )

    experience_html = "".join(
        f'<li class="timeline-item">{_text(item)}</li>'
        for item in experience
        if str(item).strip()
    )

    education_html = "".join(
        f'<li class="timeline-item">{_text(item)}</li>'
        for item in education
        if str(item).strip()
    )

    contact_links = ""

    if email_url:
        contact_links += (
            f'<a class="contact-link" href="{email_url}">'
            'Email Me</a>'
        )

    if linkedin_url:
        contact_links += (
            f'<a class="contact-link" href="{linkedin_url}" '
            'target="_blank" rel="noopener noreferrer">'
            'LinkedIn ↗</a>'
        )

    if website_url:
        contact_links += (
            f'<a class="contact-link" href="{website_url}" '
            'target="_blank" rel="noopener noreferrer">'
            'Website ↗</a>'
        )

    if phone:
        contact_links += (
            f'<span class="contact-link">{phone}</span>'
        )

    if location:
        contact_links += (
            f'<span class="contact-link">{location}</span>'
        )

    if not project_html:
        project_html = (
            '<p class="muted">Projects will appear here '
            'when you add them to your profile.</p>'
        )

    if not skill_html:
        skill_html = '<p class="muted">No skills added yet.</p>'

    if not experience_html:
        experience_html = '<li class="timeline-item">'
        experience_html += 'No experience added yet.</li>'

    if not education_html:
        education_html = '<li class="timeline-item">'
        education_html += 'No education added yet.</li>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{summary}">
<title>{name} | Portfolio</title>

<style>
:root {{
    --background: #071426;
    --surface: #10233d;
    --surface-light: #162d4c;
    --blue: #3b82f6;
    --cyan: #38bdf8;
    --text: #edf4ff;
    --muted: #a8b8ce;
    --border: rgba(148, 183, 224, 0.17);
}}

* {{
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    margin: 0;
    background: var(--background);
    color: var(--text);
    font-family: Arial, Helvetica, sans-serif;
    line-height: 1.7;
}}

a {{
    color: inherit;
    text-decoration: none;
}}

.container {{
    width: min(1100px, 90%);
    margin: auto;
}}

nav {{
    position: sticky;
    top: 0;
    z-index: 10;
    background: rgba(7, 20, 38, 0.92);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
}}

.nav-inner {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0;
    gap: 20px;
}}

.brand {{
    font-weight: 800;
    color: var(--cyan);
    font-size: 1.15rem;
}}

.nav-links {{
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    color: var(--muted);
    font-size: 0.9rem;
}}

.nav-links a:hover {{
    color: white;
}}

.hero {{
    padding: 105px 0 85px;
    background:
        radial-gradient(
            circle at 80% 20%,
            rgba(59, 130, 246, 0.20),
            transparent 35%
        );
}}

.eyebrow {{
    color: var(--cyan);
    text-transform: uppercase;
    letter-spacing: 3px;
    font-size: 0.8rem;
    font-weight: 700;
}}

h1 {{
    font-size: clamp(2.6rem, 7vw, 5rem);
    line-height: 1.08;
    margin: 15px 0;
}}

.gradient-text {{
    background: linear-gradient(90deg, #60a5fa, #38bdf8);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}}

.hero-summary {{
    max-width: 720px;
    color: var(--muted);
    font-size: 1.1rem;
}}

.section {{
    padding: 75px 0;
}}

.section-heading {{
    margin-bottom: 30px;
}}

.section-heading h2 {{
    font-size: 2rem;
    margin-bottom: 5px;
}}

.section-heading p,
.muted {{
    color: var(--muted);
}}

.skill-list,
.technology-list,
.contact-list {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}}

.skill-tag,
.tech-tag {{
    display: inline-block;
    background: rgba(59, 130, 246, 0.13);
    border: 1px solid rgba(96, 165, 250, 0.25);
    color: #bfdbfe;
    border-radius: 30px;
    padding: 6px 12px;
    font-size: 0.82rem;
}}

.project-grid {{
    display: grid;
    grid-template-columns: repeat(
        auto-fit, minmax(min(100%, 280px), 1fr)
    );
    gap: 20px;
}}

.project-card {{
    display: flex;
    flex-direction: column;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 25px;
    transition: transform 0.25s ease, border-color 0.25s ease;
}}

.project-card:hover {{
    transform: translateY(-6px);
    border-color: var(--blue);
}}

.project-card h3 {{
    margin: 0 0 10px;
    font-size: 1.25rem;
}}

.project-description {{
    color: var(--muted);
    white-space: pre-line;
}}

.technology-list {{
    margin-top: 12px;
}}

.project-actions {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: auto;
    padding-top: 22px;
}}

.project-button,
.contact-link {{
    display: inline-block;
    border-radius: 9px;
    padding: 9px 14px;
    font-weight: 700;
    font-size: 0.88rem;
}}

.project-button.primary {{
    background: var(--blue);
    color: white;
}}

.project-button.secondary,
.contact-link {{
    border: 1px solid var(--border);
    background: var(--surface-light);
    color: var(--text);
}}

.project-button:hover,
.contact-link:hover {{
    filter: brightness(1.15);
}}

.timeline {{
    list-style: none;
    padding: 0;
}}

.timeline-item {{
    background: var(--surface);
    border-left: 3px solid var(--blue);
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin-bottom: 12px;
    white-space: pre-line;
}}

.contact-panel {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 30px;
}}

footer {{
    border-top: 1px solid var(--border);
    color: var(--muted);
    padding: 25px 0;
    text-align: center;
}}

.reveal {{
    opacity: 0;
    transform: translateY(18px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}}

.reveal.visible {{
    opacity: 1;
    transform: translateY(0);
}}

@media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
        scroll-behavior: auto !important;
        transition: none !important;
    }}

    .reveal {{
        opacity: 1;
        transform: none;
    }}
}}

@media print {{
    nav, .no-print {{
        display: none !important;
    }}

    body {{
        background: white;
        color: #111827;
    }}

    .project-card, .timeline-item, .contact-panel {{
        background: white;
        color: #111827;
        border: 1px solid #ddd;
        break-inside: avoid;
    }}

    .muted, .project-description {{
        color: #444;
    }}

    .reveal {{
        opacity: 1;
        transform: none;
    }}
}}
</style>
</head>

<body>
<nav class="no-print">
    <div class="container nav-inner">
        <a class="brand" href="#home">Career Portfolio</a>
        <div class="nav-links">
            <a href="#about">About</a>
            <a href="#skills">Skills</a>
            <a href="#projects">Projects</a>
            <a href="#experience">Experience</a>
            <a href="#contact">Contact</a>
        </div>
    </div>
</nav>

<header class="hero" id="home">
    <div class="container reveal">
        <div class="eyebrow">Hello, I'm</div>
        <h1><span class="gradient-text">{name}</span></h1>
        <p class="hero-summary">{summary}</p>
        <button class="project-button primary no-print"
                onclick="window.print()">
            Print / Save as PDF
        </button>
    </div>
</header>

<main>
    <section class="section" id="about">
        <div class="container reveal">
            <div class="section-heading">
                <h2>About Me</h2>
                <p>A little about my professional journey.</p>
            </div>
            <p>{summary}</p>
        </div>
    </section>

    <section class="section" id="skills">
        <div class="container reveal">
            <div class="section-heading">
                <h2>Skills</h2>
                <p>Tools and technologies I work with.</p>
            </div>
            <div class="skill-list">{skill_html}</div>
        </div>
    </section>

    <section class="section" id="projects">
        <div class="container">
            <div class="section-heading reveal">
                <h2>Featured Projects</h2>
                <p>Some things I've built and worked on.</p>
            </div>
            <div class="project-grid">{project_html}</div>
        </div>
    </section>

    <section class="section" id="experience">
        <div class="container reveal">
            <div class="section-heading">
                <h2>Experience</h2>
            </div>
            <ul class="timeline">{experience_html}</ul>
        </div>
    </section>

    <section class="section" id="education">
        <div class="container reveal">
            <div class="section-heading">
                <h2>Education</h2>
            </div>
            <ul class="timeline">{education_html}</ul>
        </div>
    </section>

    <section class="section" id="contact">
        <div class="container reveal">
            <div class="section-heading">
                <h2>Let's Connect</h2>
                <p>Feel free to get in touch.</p>
            </div>
            <div class="contact-panel">
                <div class="contact-list">{contact_links}</div>
            </div>
        </div>
    </section>
</main>

<footer>
    <div class="container">
        © {name} · Built with CareerForge AI
    </div>
</footer>

<script>
(function () {{
    const elements = document.querySelectorAll(".reveal");

    if (!("IntersectionObserver" in window)) {{
        elements.forEach(element => element.classList.add("visible"));
        return;
    }}

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                entry.target.classList.add("visible");
                observer.unobserve(entry.target);
            }}
        }});
    }}, {{ threshold: 0.12 }});

    elements.forEach(element => observer.observe(element));
}})();
</script>
</body>
</html>
"""
