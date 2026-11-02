
import html
import json
import re


def _safe(value):
    """Escape user-provided text before inserting it into HTML."""
    return html.escape(str(value or "").strip(), quote=True)


def _safe_url(value):
    """Allow only safe HTTP, HTTPS, and mailto links."""
    value = str(value or "").strip()

    if not value:
        return ""

    if re.match(r"^https?://", value, re.IGNORECASE):
        return value if not any(ord(c) < 32 for c in value) else ""

    if re.match(r"^mailto:", value, re.IGNORECASE):
        return value if not any(ord(c) < 32 for c in value) else ""

    return ""


def _get_list(profile, key):
    """Return a clean list from the existing profile schema."""
    value = profile.get(key, [])

    if isinstance(value, str):
        value = value.splitlines()

    if not isinstance(value, (list, tuple)):
        return []

    return [
        str(item).strip()
        for item in value
        if item and str(item).strip()
    ]


def _social_links(profile):
    """Build social links from existing profile fields."""
    links = []

    linkedin = _safe_url(profile.get("linkedin"))
    website = _safe_url(profile.get("website"))
    email = str(profile.get("email", "")).strip()

    if linkedin:
        links.append(("LinkedIn", linkedin))

    if website:
        links.append(("Website", website))

    if email and re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+",
        email
    ):
        links.append(("Email", "mailto:" + email))

    return links


def _project_card(project, index):
    """
    Create a project card.

    Existing profile schema stores projects as text entries,
    so each entry becomes a project card.
    """
    text = _safe(project)

    return f"""
        <article class="project-card reveal">
            <div class="project-number">PROJECT {index:02d}</div>
            <h3>{text}</h3>
            <div class="project-line"></div>
        </article>
    """


def _list_items(items, css_class):
    """Create escaped list entries."""
    if not items:
        return ""

    return "".join(
        f'<li class="{css_class}">{_safe(item)}</li>'
        for item in items
    )


def generate_portfolio_html(profile):
    """
    Generate a complete responsive HTML portfolio.

    Compatible with the existing CareerForge AI profile schema:

    name, email, phone, location, linkedin, website,
    summary, skills, experience, education, projects.
    """

    if not isinstance(profile, dict):
        raise TypeError("Profile must be a dictionary.")

    name = str(profile.get("name", "")).strip()

    if not name:
        raise ValueError(
            "A name is required to generate your portfolio."
        )

    safe_name = _safe(name)
    email = str(profile.get("email", "")).strip()
    phone = str(profile.get("phone", "")).strip()
    location = str(profile.get("location", "")).strip()
    summary = str(profile.get("summary", "")).strip()

    safe_email = _safe(email)
    safe_phone = _safe(phone)
    safe_location = _safe(location)
    safe_summary = _safe(summary)

    skills = _get_list(profile, "skills")
    experience = _get_list(profile, "experience")
    education = _get_list(profile, "education")
    projects = _get_list(profile, "projects")

    social_links = _social_links(profile)

    safe_skills = "".join(
        f'<span class="skill-tag">{_safe(skill)}</span>'
        for skill in skills
    )

    project_cards = "".join(
        _project_card(project, index)
        for index, project in enumerate(projects, start=1)
    )

    experience_items = _list_items(
        experience,
        "timeline-item",
    )

    education_items = _list_items(
        education,
        "timeline-item",
    )

    social_html = "".join(
        f"""
        <a class="social-link"
           href="{_safe_url(url)}"
           target="_blank"
           rel="noopener noreferrer">
            {_safe(label)}
            <span aria-hidden="true">↗</span>
        </a>
        """
        for label, url in social_links
    )

    contact_parts = []

    if email and re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+",
        email
    ):
        contact_parts.append(
            f"""
            <a href="mailto:{_safe(email)}" class="contact-link">
                {safe_email}
            </a>
            """
        )

    if phone:
        safe_phone_href = re.sub(r"[^0-9+]", "", phone)

        if safe_phone_href:
            contact_parts.append(
                f"""
                <a href="tel:{_safe(safe_phone_href)}"
                   class="contact-link">
                    {safe_phone}
                </a>
                """
            )

    contact_html = "".join(contact_parts)

    if not contact_html:
        contact_html = (
            '<p class="muted">Add your email or phone number '
            'to your CareerForge profile to display contact details.</p>'
        )

    if not safe_summary:
        safe_summary = (
            "Welcome to my professional portfolio. "
            "Explore my skills, projects, and experience."
        )

    if not safe_skills:
        safe_skills = (
            '<p class="muted">Add skills to your profile to '
            'showcase them here.</p>'
        )

    if not project_cards:
        project_cards = (
            '<p class="muted">Projects will appear here after '
            'you add them to your profile.</p>'
        )

    if not experience_items:
        experience_items = (
            '<li class="muted">Professional experience has '
            'not been added yet.</li>'
        )

    if not education_items:
        education_items = (
            '<li class="muted">Education details have '
            'not been added yet.</li>'
        )

    if not social_html:
        social_html = (
            '<span class="muted">Add LinkedIn or website links '
            'to your profile.</span>'
        )

    # The generated document is self-contained.
    # No external JavaScript library is required.
    # The resume button can download the resume only when
    # a resume PDF is supplied separately.

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <meta name="description"
          content="Professional portfolio of {safe_name}">

    <meta name="author" content="{safe_name}">

    <title>{safe_name} | Professional Portfolio</title>

    <style>
        :root {{
            --background: #081225;
            --background-soft: #0d1b33;
            --surface: #12213b;
            --surface-light: #182c4b;
            --primary: #4f8cff;
            --primary-light: #7eb0ff;
            --text: #f5f8ff;
            --muted: #a4b3ca;
            --border: rgba(148, 174, 215, 0.17);
            --shadow: 0 18px 50px rgba(0, 0, 0, 0.20);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            background: var(--background);
            color: var(--text);
            font-family: Inter, Arial, sans-serif;
            line-height: 1.7;
            overflow-x: hidden;
        }}

        a {{
            color: inherit;
            text-decoration: none;
        }}

        .container {{
            width: min(1120px, 90%);
            margin: auto;
        }}

        .navbar {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(8, 18, 37, 0.90);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border);
        }}

        .nav-inner {{
            min-height: 72px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }}

        .logo {{
            font-size: 21px;
            font-weight: 800;
            letter-spacing: -0.7px;
        }}

        .logo span {{
            color: var(--primary-light);
        }}

        .nav-links {{
            display: flex;
            align-items: center;
            gap: 25px;
            flex-wrap: wrap;
        }}

        .nav-links a {{
            color: var(--muted);
            font-size: 13px;
            transition: color 0.2s ease;
        }}

        .nav-links a:hover {{
            color: white;
        }}

        .hero {{
            min-height: 590px;
            display: flex;
            align-items: center;
            position: relative;
            overflow: hidden;
            padding: 100px 0;
        }}

        .hero::before {{
            content: "";
            position: absolute;
            width: 430px;
            height: 430px;
            right: -100px;
            top: 30px;
            border-radius: 50%;
            background: rgba(56, 117, 255, 0.17);
            filter: blur(80px);
            pointer-events: none;
        }}

        .hero-content {{
            position: relative;
            z-index: 1;
            max-width: 780px;
        }}

        .eyebrow {{
            display: inline-flex;
            align-items: center;
            gap: 9px;
            color: var(--primary-light);
            background: rgba(79, 140, 255, 0.10);
            border: 1px solid rgba(79, 140, 255, 0.25);
            padding: 8px 14px;
            border-radius: 30px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1.3px;
            text-transform: uppercase;
            margin-bottom: 25px;
        }}

        .eyebrow::before {{
            content: "";
            width: 7px;
            height: 7px;
            background: #63e6a5;
            border-radius: 50%;
        }}

        .hero h1 {{
            font-size: clamp(42px, 7vw, 76px);
            line-height: 1.08;
            letter-spacing: -3px;
            font-weight: 800;
            margin-bottom: 25px;
            overflow-wrap: anywhere;
        }}

        .hero h1 span {{
            color: var(--primary-light);
        }}

        .hero-description {{
            max-width: 650px;
            color: var(--muted);
            font-size: 17px;
            margin-bottom: 32px;
        }}

        .hero-actions {{
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
        }}

        .button {{
            display: inline-flex;
            justify-content: center;
            align-items: center;
            gap: 9px;
            border-radius: 9px;
            padding: 13px 21px;
            font-size: 14px;
            font-weight: 700;
            transition: transform 0.25s ease,
                        background 0.25s ease,
                        border-color 0.25s ease;
        }}

        .button:hover {{
            transform: translateY(-3px);
        }}

        .button-primary {{
            color: white;
            background: var(--primary);
            box-shadow: 0 8px 25px rgba(79, 140, 255, 0.25);
        }}

        .button-primary:hover {{
            background: #3479f5;
        }}

        .button-outline {{
            border: 1px solid var(--border);
            color: white;
        }}

        .button-outline:hover {{
            border-color: var(--primary);
            background: rgba(79, 140, 255, 0.10);
        }}

        section {{
            padding: 85px 0;
            border-top: 1px solid var(--border);
        }}

        .section-label {{
            color: var(--primary-light);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 800;
            margin-bottom: 12px;
        }}

        .section-title {{
            font-size: clamp(28px, 4vw, 42px);
            font-weight: 800;
            letter-spacing: -1.4px;
            margin-bottom: 15px;
        }}

        .section-description {{
            color: var(--muted);
            max-width: 650px;
            margin-bottom: 35px;
        }}

        .about-box {{
            background: linear-gradient(
                135deg,
                var(--surface),
                var(--background-soft)
            );
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 35px;
            box-shadow: var(--shadow);
        }}

        .about-box p {{
            color: var(--muted);
            font-size: 16px;
            white-space: pre-line;
        }}

        .skills-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .skill-tag {{
            background: var(--surface);
            border: 1px solid var(--border);
            color: #dce8ff;
            padding: 11px 17px;
            border-radius: 9px;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.25s ease;
        }}

        .skill-tag:hover {{
            border-color: var(--primary);
            color: white;
            transform: translateY(-3px);
        }}

        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 20px;
        }}

        .project-card {{
            position: relative;
            overflow: hidden;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 27px;
            min-height: 175px;
            transition: transform 0.3s ease,
                        border-color 0.3s ease,
                        box-shadow 0.3s ease;
        }}

        .project-card:hover {{
            transform: translateY(-6px);
            border-color: rgba(79, 140, 255, 0.7);
            box-shadow: var(--shadow);
        }}

        .project-number {{
            color: var(--primary-light);
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.5px;
            margin-bottom: 20px;
        }}

        .project-card h3 {{
            font-size: 18px;
            line-height: 1.5;
            overflow-wrap: anywhere;
        }}

        .project-line {{
            width: 35px;
            height: 3px;
            border-radius: 10px;
            background: var(--primary);
            margin-top: 23px;
        }}

        .timeline {{
            list-style: none;
            display: grid;
            gap: 15px;
        }}

        .timeline-item {{
            position: relative;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 13px;
            padding: 20px 22px 20px 45px;
            color: #dce8ff;
            overflow-wrap: anywhere;
        }}

        .timeline-item::before {{
            content: "";
            position: absolute;
            left: 20px;
            top: 27px;
            width: 9px;
            height: 9px;
            background: var(--primary);
            border-radius: 50%;
        }}

        .social-links {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }}

        .social-link {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: var(--surface);
            border: 1px solid var(--border);
            padding: 12px 17px;
            border-radius: 9px;
            color: #dce8ff;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}

        .social-link:hover {{
            border-color: var(--primary);
            color: white;
            transform: translateY(-3px);
        }}

        .contact-box {{
            text-align: center;
            background: linear-gradient(
                135deg,
                #142c50,
                #1c3c70
            );
            border: 1px solid rgba(126, 176, 255, 0.25);
            border-radius: 20px;
            padding: 55px 25px;
        }}

        .contact-box .section-description {{
            margin: 0 auto 25px;
        }}

        .contact-details {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 25px;
        }}

        .contact-link {{
            color: #dce8ff;
            border: 1px solid rgba(255,255,255,0.2);
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 13px;
            overflow-wrap: anywhere;
        }}

        .contact-link:hover {{
            border-color: var(--primary-light);
        }}

        .muted {{
            color: var(--muted);
            font-size: 14px;
        }}

        footer {{
            padding: 30px 0;
            border-top: 1px solid var(--border);
            text-align: center;
            color: var(--muted);
            font-size: 12px;
        }}

        .reveal {{
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.65s ease,
                        transform 0.65s ease;
        }}

        .reveal.visible {{
            opacity: 1;
            transform: translateY(0);
        }}

        @media (max-width: 700px) {{
            .nav-inner {{
                padding: 15px 0;
                align-items: flex-start;
                flex-direction: column;
            }}

            .nav-links {{
                gap: 13px;
            }}

            .hero {{
                min-height: auto;
                padding: 85px 0;
            }}

            .hero h1 {{
                letter-spacing: -1.5px;
            }}

            .hero-description {{
                font-size: 15px;
            }}

            section {{
                padding: 65px 0;
            }}

            .projects-grid {{
                grid-template-columns: 1fr;
            }}

            .about-box {{
                padding: 24px;
            }}

            .contact-box {{
                padding: 38px 20px;
            }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            *,
            *::before,
            *::after {{
                scroll-behavior: auto !important;
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }}

            .reveal {{
                opacity: 1;
                transform: none;
            }}
        }}

        @media print {{
            .navbar,
            .hero-actions,
            .social-links {{
                display: none;
            }}

            body {{
                background: white;
                color: #111;
            }}

            section {{
                border-color: #ddd;
            }}

            .section-title,
            .project-card h3 {{
                color: #111;
            }}
        }}
    </style>
</head>

<body>

    <header class="navbar">
        <div class="container nav-inner">
            <a class="logo" href="#home">
                {safe_name.split(" ")[0]}<span>.</span>
            </a>

            <nav class="nav-links" aria-label="Main navigation">
                <a href="#about">About</a>
                <a href="#skills">Skills</a>
                <a href="#projects">Projects</a>
                <a href="#experience">Experience</a>
                <a href="#contact">Contact</a>
            </nav>
        </div>
    </header>

    <main>

        <section class="hero" id="home">
            <div class="container">
                <div class="hero-content reveal">

                    <div class="eyebrow">
                        Professional Portfolio
                    </div>

                    <h1>
                        Hi, I'm <span>{safe_name}</span>
                    </h1>

                    <p class="hero-description">
                        {safe_summary}
                    </p>

                    <div class="hero-actions">
                        <a class="button button-primary"
                           href="#projects">
                            Explore My Work
                            <span aria-hidden="true">→</span>
                        </a>

                        <a class="button button-outline"
                           href="#contact">
                            Contact Me
                        </a>

                        <button class="button button-outline"
                                type="button"
                                onclick="window.print()">
                            Download / Print Resume
                        </button>
                    </div>

                    <p class="muted" style="margin-top:20px;">
                        {safe_location}
                    </p>

                </div>
            </div>
        </section>


        <section id="about">
            <div class="container reveal">

                <div class="section-label">Introduction</div>

                <h2 class="section-title">
                    About Me
                </h2>

                <p class="section-description">
                    A little more about my professional journey.
                </p>

                <div class="about-box">
                    <p>{safe_summary}</p>
                </div>

            </div>
        </section>


        <section id="skills">
            <div class="container reveal">

                <div class="section-label">What I Work With</div>

                <h2 class="section-title">
                    Skills & Expertise
                </h2>

                <p class="section-description">
                    Technologies, tools, and abilities I bring
                    to my work.
                </p>

                <div class="skills-grid">
                    {safe_skills}
                </div>

            </div>
        </section>


        <section id="projects">
            <div class="container">

                <div class="reveal">
                    <div class="section-label">Selected Work</div>

                    <h2 class="section-title">
                        Featured Projects
                    </h2>

                    <p class="section-description">
                        A selection of projects and work from
                        my professional journey.
                    </p>
                </div>

                <div class="projects-grid">
                    {project_cards}
                </div>

            </div>
        </section>


        <section id="experience">
            <div class="container">

                <div class="reveal">
                    <div class="section-label">My Journey</div>

                    <h2 class="section-title">
                        Experience
                    </h2>

                    <p class="section-description">
                        Professional experience and key contributions.
                    </p>
                </div>

                <ul class="timeline reveal">
                    {experience_items}
                </ul>

            </div>
        </section>


        <section id="education">
            <div class="container">

                <div class="reveal">
                    <div class="section-label">Learning</div>

                    <h2 class="section-title">
                        Education
                    </h2>

                    <p class="section-description">
                        My academic background and learning journey.
                    </p>
                </div>

                <ul class="timeline reveal">
                    {education_items}
                </ul>

            </div>
        </section>


        <section id="social">
            <div class="container reveal">

                <div class="section-label">Find Me Online</div>

                <h2 class="section-title">
                    Social & Professional Links
                </h2>

                <p class="section-description">
                    Connect with me and explore my professional presence.
                </p>

                <div class="social-links">
                    {social_html}
                </div>

            </div>
        </section>


        <section id="contact">
            <div class="container">

                <div class="contact-box reveal">

                    <div class="section-label">
                        Get In Touch
                    </div>

                    <h2 class="section-title">
                        Let's Work Together
                    </h2>

                    <p class="section-description">
                        Interested in working together or discussing
                        an opportunity? Feel free to get in touch.
                    </p>

                    <div class="hero-actions"
                         style="justify-content:center;">

                        {(
                            f'<a class="button button-primary" '
                            f'href="mailto:{_safe(email)}">'
                            f'Send Me an Email</a>'
                        ) if email and re.fullmatch(
                            r"[^@\s]+@[^@\s]+\.[^@\s]+", email
                        ) else ""}

                    </div>

                    <div class="contact-details">
                        {contact_html}
                    </div>

                </div>

            </div>
        </section>

    </main>


    <footer>
        <div class="container">
            © <span id="year"></span> {safe_name}.
            Built with CareerForge AI.
        </div>
    </footer>


    <script>
        document.getElementById("year").textContent =
            new Date().getFullYear();

        const revealElements =
            document.querySelectorAll(".reveal");

        if ("IntersectionObserver" in window) {{
            const observer = new IntersectionObserver(
                (entries) => {{
                    entries.forEach((entry) => {{
                        if (entry.isIntersecting) {{
                            entry.target.classList.add("visible");
                            observer.unobserve(entry.target);
                        }}
                    }});
                }},
                {{ threshold: 0.12 }}
            );

            revealElements.forEach((element) => {{
                observer.observe(element);
            }});
        }} else {{
            revealElements.forEach((element) => {{
                element.classList.add("visible");
            }});
        }}
    </script>

</body>
</html>
"""

    return document

