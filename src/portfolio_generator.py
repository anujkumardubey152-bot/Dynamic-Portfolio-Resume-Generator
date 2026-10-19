
from html import escape
from pathlib import Path
from urllib.parse import urlparse


def _text(value):
    """Safely convert a value to HTML text."""
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple, set)):
        return escape(", ".join(str(item) for item in value))
    return escape(str(value).strip())


def _url(value, schemes=("http", "https")):
    """Normalize and validate a URL before placing it in an HTML link."""
    raw = str(value or "").strip()
    if not raw:
        return ""

    if raw.startswith("//"):
        raw = "https:" + raw
    elif "://" not in raw and not raw.lower().startswith("mailto:"):
        raw = "https://" + raw

    try:
        parsed = urlparse(raw)
    except ValueError:
        return ""

    if parsed.scheme.lower() not in schemes:
        return ""

    if parsed.scheme.lower() in ("http", "https"):
        if not parsed.hostname or "." not in parsed.hostname:
            return ""
        if any(char.isspace() for char in parsed.netloc):
            return ""

    return escape(raw, quote=True)


def _items(value):
    """Normalize list-like profile fields."""
    if value is None or value == "":
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.splitlines() if item.strip()]
    if isinstance(value, dict):
        return [value]
    try:
        return list(value)
    except TypeError:
        return [value]


def _skills(value):
    """Support both a list of skills and categorized skill dictionaries."""
    if isinstance(value, dict):
        result = []
        for category, values in value.items():
            if isinstance(values, str):
                values = [part.strip() for part in values.split(",") if part.strip()]
            else:
                values = _items(values)
            for skill in values:
                if isinstance(skill, dict):
                    skill = skill.get("name") or skill.get("skill") or ""
                if str(skill).strip():
                    result.append((str(category).strip(), str(skill).strip()))
        return result

    result = []
    for skill in _items(value):
        if isinstance(skill, dict):
            category = skill.get("category", "")
            name = skill.get("name") or skill.get("skill") or ""
            if name:
                result.append((str(category).strip(), str(name).strip()))
        elif str(skill).strip():
            result.append(("", str(skill).strip()))
    return result


def _link(label, value, css_class="text-link"):
    """Build a safe external link, or plain text if the URL is invalid."""
    safe_url = _url(value)
    if not safe_url:
        return _text(label)
    return (
        f'<a class="{css_class}" href="{safe_url}" '
        'target="_blank" rel="noopener noreferrer">'
        f'{_text(label)}</a>'
    )


def _section(title, content, section_id=None, eyebrow=None):
    """Render a portfolio section only when it contains content."""
    if not content:
        return ""

    safe_id = f' id="{escape(section_id, quote=True)}"' if section_id else ""
    eyebrow_html = (
        f'<p class="section-kicker">{_text(eyebrow)}</p>'
        if eyebrow else ""
    )
    return f"""
    <section class="section"{safe_id}>
      {eyebrow_html}
      <h2>{_text(title)}</h2>
      <div class="section-content">{content}</div>
    </section>
    """


def _date_text(item):
    start = item.get("start_date") or item.get("start") or ""
    end = item.get("end_date") or item.get("end") or ""
    dates = item.get("dates") or item.get("duration") or ""

    if dates:
        return _text(dates)

    if start and end:
        return f"{_text(start)} — {_text(end)}"
    if start:
        return f"{_text(start)} — Present"
    return _text(end)


def _bullet_list(value):
    """Render achievements or descriptions as a semantic list."""
    if isinstance(value, str):
        lines = [line.strip(" •-\t") for line in value.splitlines() if line.strip()]
        if len(lines) <= 1:
            return f"<p>{_text(value)}</p>" if value.strip() else ""
        items = lines
    else:
        items = _items(value)

    rendered = []
    for item in items:
        if isinstance(item, dict):
            item = item.get("text") or item.get("description") or item.get("achievement") or ""
        if str(item).strip():
            rendered.append(f"<li>{_text(item)}</li>")

    if not rendered:
        return ""
    if len(rendered) == 1:
        return f"<p>{rendered[0][4:-5]}</p>"
    return '<ul class="detail-list">' + "".join(rendered) + "</ul>"


def _contact_link(label, value, kind="url"):
    """Build contact links while preserving a clean contact row."""
    raw = str(value or "").strip()
    if not raw:
        return ""

    if kind == "email":
        safe_value = escape(raw, quote=True)
        return f'<a href="mailto:{safe_value}">{_text(raw)}</a>'

    if kind == "phone":
        safe_value = escape(raw, quote=True)
        phone_number = "".join(c for c in raw if c.isdigit() or c == "+")
        return f'<a href="tel:{escape(phone_number, quote=True)}">{_text(raw)}</a>'

    return _link(label, raw)


def generate_portfolio_html(profile):
    """Generate a premium, responsive, standalone HTML portfolio."""
    profile = profile or {}

    name = _text(
        profile.get("name") or profile.get("full_name")
        or profile.get("candidate_name")
    ) or "Your Name"

    headline = _text(
        profile.get("headline") or profile.get("professional_title")
        or profile.get("job_title") or profile.get("title")
    )

    summary = _text(
        profile.get("summary") or profile.get("professional_summary")
        or profile.get("about") or profile.get("objective")
    )

    email = profile.get("email") or profile.get("email_address")
    phone = profile.get("phone") or profile.get("phone_number")
    location = _text(profile.get("location") or profile.get("city"))
    linkedin = profile.get("linkedin") or profile.get("linkedin_url")
    github = profile.get("github") or profile.get("github_url")
    website = profile.get("website") or profile.get("website_url") or profile.get("portfolio")

    skills = _skills(profile.get("skills") or profile.get("technical_skills"))
    experience = _items(profile.get("experience") or profile.get("work_experience"))
    education = _items(profile.get("education"))
    projects = _items(profile.get("projects") or profile.get("personal_projects"))

    contact_parts = []
    email_html = _contact_link("Email", email, "email")
    phone_html = _contact_link("Phone", phone, "phone")

    if email_html:
        contact_parts.append(email_html)
    if phone_html:
        contact_parts.append(phone_html)
    if location:
        contact_parts.append(f"<span>{location}</span>")

    contact_html = '<span class="contact-item">' + (
        '</span><span class="contact-dot">•</span><span class="contact-item">'.join(contact_parts)
    ) + "</span>" if contact_parts else ""

    social_links = []
    for label, value in (
        ("LinkedIn", linkedin),
        ("GitHub", github),
        ("Website", website),
    ):
        link = _link(label, value, "social-link")
        if value and link != _text(label):
            social_links.append(link)

    social_html = "".join(social_links)

    skill_groups = {}
    for category, skill in skills:
        group = category or "Core Skills"
        skill_groups.setdefault(group, [])
        skill_groups[group].append(skill)

    skills_html = ""
    for category, values in skill_groups.items():
        badges = "".join(
            f'<span class="skill">{_text(skill)}</span>'
            for skill in values
        )
        skills_html += f"""
        <div class="skill-group">
          <h3>{_text(category)}</h3>
          <div class="skills">{badges}</div>
        </div>
        """

    experience_html = ""
    for item in experience:
        if isinstance(item, dict):
            title = _text(item.get("title") or item.get("role") or item.get("position") or "Experience")
            company = _text(item.get("company") or item.get("organization"))
            dates = _date_text(item)
            place = _text(item.get("location"))
            description = item.get("achievements") or item.get("responsibilities") or item.get("description") or ""
        else:
            title = "Experience"
            company = ""
            dates = ""
            place = ""
            description = item

        meta = " · ".join(part for part in (company, place) if part)
        meta_html = f'<p class="entry-meta">{meta}</p>' if meta else ""
        dates_html = f'<span class="entry-date">{dates}</span>' if dates else ""

        experience_html += f"""
        <article class="timeline-entry">
          <span class="timeline-marker" aria-hidden="true"></span>
          <div class="entry-heading">
            <h3>{title}</h3>
            {dates_html}
          </div>
          {meta_html}
          <div class="entry-description">{_bullet_list(description)}</div>
        </article>
        """

    education_html = ""
    for item in education:
        if isinstance(item, dict):
            title = _text(item.get("degree") or item.get("title") or item.get("qualification") or "Education")
            institution = _text(item.get("institution") or item.get("school") or item.get("university"))
            dates = _date_text(item) or _text(item.get("year"))
            details = item.get("description") or item.get("grade") or item.get("details") or ""
        else:
            title, institution, dates, details = _text(item), "", "", ""

        meta = " · ".join(part for part in (institution, dates) if part)
        education_html += f"""
        <article class="simple-entry">
          <h3>{title}</h3>
          {f'<p class="entry-meta">{meta}</p>' if meta else ""}
          {f'<p class="entry-description">{_text(details)}</p>' if details else ""}
        </article>
        """

    projects_html = ""
    for item in projects:
        if isinstance(item, dict):
            title = _text(item.get("name") or item.get("title") or "Project")
            description = _text(item.get("description") or item.get("summary"))
            link = item.get("link") or item.get("url") or item.get("live_demo")
            repo = item.get("github") or item.get("github_url") or item.get("repository")
            technologies = item.get("technologies") or item.get("tech") or item.get("tools") or []
            if isinstance(technologies, str):
                technologies = [part.strip() for part in technologies.split(",") if part.strip()]
            else:
                technologies = _items(technologies)
        else:
            title = "Project"
            description = _text(item)
            link, repo, technologies = "", "", []

        technology_html = "".join(
            f'<span class="project-tech">{_text(tech)}</span>'
            for tech in technologies if str(tech).strip()
        )

        actions = []
        safe_live = _url(link)
        safe_repo = _url(repo)
        if safe_live:
            actions.append(
                f'<a class="project-action" href="{safe_live}" '
                'target="_blank" rel="noopener noreferrer">Live project ↗</a>'
            )
        if safe_repo:
            actions.append(
                f'<a class="project-action secondary-action" href="{safe_repo}" '
                'target="_blank" rel="noopener noreferrer">Source code ↗</a>'
            )

        projects_html += f"""
        <article class="project-card">
          <div class="project-topline">
            <span class="project-symbol" aria-hidden="true">↗</span>
            <span class="project-label">FEATURED PROJECT</span>
          </div>
          <h3>{title}</h3>
          <p class="project-description">{description}</p>
          {f'<div class="project-tech-list">{technology_html}</div>' if technology_html else ""}
          {f'<div class="project-actions">{"".join(actions)}</div>' if actions else ""}
        </article>
        """

    sections = [
        _section("Skills & Expertise", skills_html, "skills", "WHAT I BRING"),
        _section("Experience", experience_html, "experience", "MY JOURNEY"),
        _section("Selected Projects", projects_html, "projects", "WORK & CREATIONS"),
        _section("Education", education_html, "education", "LEARNING"),
    ]

    navigation_items = [
        ("About", "about", bool(summary)),
        ("Skills", "skills", bool(skills_html)),
        ("Experience", "experience", bool(experience_html)),
        ("Projects", "projects", bool(projects_html)),
        ("Education", "education", bool(education_html)),
    ]
    navigation = "".join(
        f'<a href="#{anchor}">{label}</a>'
        for label, anchor, enabled in navigation_items if enabled
    )

    about_html = _section(
        "A little about me",
        f'<p class="about-copy">{summary}</p>',
        "about",
        "INTRODUCTION",
    ) if summary else ""

    footer_contact = ""
    if email:
        footer_contact = _contact_link("Get in touch", email, "email")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#10172a">
<meta name="description" content="{escape((summary or f'Portfolio of {name}').replace(chr(10), ' ')[:155], quote=True)}">
<title>{name} | Portfolio</title>
<style>
:root {{
  color-scheme: light;
  --ink: #172033;
  --ink-soft: #35415a;
  --muted: #667085;
  --accent: #5145cd;
  --accent-dark: #3930a3;
  --accent-soft: #eeedff;
  --surface: #ffffff;
  --background: #f6f7fb;
  --border: #e5e8f0;
  --hero: #10172a;
  --radius: 20px;
  --shadow: 0 12px 38px rgba(23, 32, 51, .055);
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; scroll-padding-top: 90px; }}
body {{
  margin: 0;
  background: var(--background);
  color: var(--ink);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system,
               BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}}
a {{ color: var(--accent); text-underline-offset: 4px; }}
a:focus-visible {{
  outline: 3px solid #9c96ff;
  outline-offset: 4px;
  border-radius: 4px;
}}
.container {{
  width: min(1040px, calc(100% - 44px));
  margin: 36px auto;
}}
.site-nav {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 18px;
  padding: 12px 4px;
}}
.brand {{
  color: var(--ink);
  font-weight: 800;
  font-size: .98rem;
  letter-spacing: -.035em;
  text-decoration: none;
  overflow-wrap: anywhere;
}}
.nav-links {{
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 8px 20px;
}}
.nav-links a {{
  color: var(--muted);
  font-size: .88rem;
  font-weight: 600;
  text-decoration: none;
  transition: color .18s ease;
}}
.nav-links a:hover {{ color: var(--accent); }}
.hero {{
  position: relative;
  isolation: isolate;
  overflow: hidden;
  padding: clamp(34px, 7vw, 76px);
  border: 1px solid rgba(255,255,255,.08);
  border-radius: 28px;
  background:
    radial-gradient(ellipse at 88% 12%, rgba(99, 91, 255, .26), transparent 35%),
    radial-gradient(ellipse at 8% 100%, rgba(54, 89, 180, .18), transparent 38%),
    var(--hero);
  color: #fff;
  box-shadow: 0 24px 70px rgba(16, 23, 42, .16);
}}
.hero::after {{
  content: "";
  position: absolute;
  z-index: -1;
  inset: 0;
  opacity: .14;
  background-image: radial-gradient(rgba(255,255,255,.35) .7px, transparent .7px);
  background-size: 19px 19px;
  mask-image: linear-gradient(120deg, black, transparent 72%);
}}
.eyebrow, .section-kicker {{
  margin: 0 0 10px;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: .16em;
  font-size: .72rem;
  font-weight: 800;
}}
.hero .eyebrow {{ color: #b8b4ff; }}
h1 {{
  max-width: 820px;
  margin: 0;
  font-size: clamp(2.5rem, 7vw, 5.2rem);
  line-height: 1.04;
  letter-spacing: -.065em;
  overflow-wrap: anywhere;
}}
.headline {{
  max-width: 700px;
  margin: 18px 0 0;
  color: #d7def0;
  font-size: clamp(1.05rem, 2.5vw, 1.35rem);
  font-weight: 550;
}}
.hero-summary {{
  max-width: 720px;
  margin: 18px 0 0;
  color: #c0c9dc;
  font-size: 1rem;
}}
.hero-bottom {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 30px;
}}
.contact {{
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 12px;
  color: #d5dced;
  font-size: .88rem;
  overflow-wrap: anywhere;
}}
.contact a {{ color: #e0deff; text-decoration: none; }}
.contact a:hover {{ text-decoration: underline; }}
.contact-dot {{ color: #77839b; }}
.social-links {{ display: flex; flex-wrap: wrap; gap: 9px; }}
.social-link {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 38px;
  padding: 8px 13px;
  border: 1px solid rgba(255,255,255,.2);
  border-radius: 999px;
  color: #f0efff;
  background: rgba(255,255,255,.055);
  font-size: .82rem;
  font-weight: 650;
  text-decoration: none;
  transition: background .18s ease, transform .18s ease;
}}
.social-link:hover {{ background: rgba(255,255,255,.13); transform: translateY(-1px); }}
.section {{
  margin-top: 22px;
  padding: clamp(24px, 4vw, 38px);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: var(--shadow);
}}
.section-kicker {{ margin-bottom: 5px; }}
.section h2 {{
  margin: 0 0 24px;
  font-size: clamp(1.4rem, 3vw, 1.85rem);
  line-height: 1.25;
  letter-spacing: -.045em;
}}
.section h2::after {{
  content: "";
  display: block;
  width: 42px;
  height: 3px;
  margin-top: 13px;
  border-radius: 5px;
  background: linear-gradient(90deg, var(--accent), #aaa4ff);
}}
.section-content > :first-child {{ margin-top: 0; }}
.section-content > :last-child {{ margin-bottom: 0; }}
.about-copy {{ max-width: 820px; margin: 0; color: var(--ink-soft); }}
.skill-group + .skill-group {{ margin-top: 22px; }}
.skill-group h3 {{
  margin: 0 0 11px;
  color: var(--muted);
  font-size: .83rem;
  font-weight: 750;
  letter-spacing: .015em;
}}
.skills {{ display: flex; flex-wrap: wrap; gap: 9px; }}
.skill {{
  display: inline-flex;
  align-items: center;
  padding: 7px 12px;
  border: 1px solid #e3e1ff;
  border-radius: 9px;
  background: #f6f5ff;
  color: #39328f;
  font-size: .88rem;
  font-weight: 600;
}}
.timeline-entry {{
  position: relative;
  margin-left: 7px;
  padding: 0 0 26px 25px;
  border-left: 1px solid #dcdff0;
}}
.timeline-entry:last-child {{ padding-bottom: 0; border-left-color: transparent; }}
.timeline-marker {{
  position: absolute;
  top: 6px;
  left: -5px;
  width: 9px;
  height: 9px;
  border: 2px solid #fff;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 0 2px #dcd9ff;
}}
.entry-heading {{
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 6px 14px;
}}
.entry h3, .simple-entry h3 {{
  margin: 0;
  font-size: 1.04rem;
  line-height: 1.5;
  letter-spacing: -.018em;
}}
.entry-date {{
  color: var(--muted);
  font-size: .83rem;
  font-weight: 600;
}}
.entry-meta {{ margin: 3px 0 9px; color: var(--accent-dark); font-size: .9rem; font-weight: 650; }}
.entry-description {{ color: var(--ink-soft); }}
.entry-description p {{ margin: 8px 0 0; }}
.detail-list {{ margin: 8px 0 0; padding-left: 20px; color: var(--ink-soft); }}
.detail-list li {{ padding-left: 3px; margin: 5px 0; }}
.detail-list li::marker {{ color: var(--accent); }}
.simple-entry + .simple-entry {{
  margin-top: 20px;
  padding-top: 19px;
  border-top: 1px solid var(--border);
}}
.simple-entry .entry-meta {{ margin-bottom: 0; }}
.project-grid {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}}
.project-card {{
  display: flex;
  flex-direction: column;
  min-width: 0;
  padding: 23px;
  border: 1px solid var(--border);
  border-radius: 16px;
  background: linear-gradient(145deg, #fff, #fbfbff);
  transition: border-color .2s ease, box-shadow .2s ease, transform .2s ease;
}}
.project-card:hover {{
  transform: translateY(-3px);
  border-color: #c9c5ff;
  box-shadow: 0 15px 35px rgba(39, 35, 110, .08);
}}
.project-topline {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; }}
.project-symbol {{
  display: grid;
  place-items: center;
  width: 37px;
  height: 37px;
  border-radius: 11px;
  background: var(--accent-soft);
  color: var(--accent);
  font-size: 1.1rem;
  font-weight: 800;
}}
.project-label {{ color: #8a90a4; font-size: .64rem; font-weight: 800; letter-spacing: .12em; }}
.project-card h3 {{ margin: 19px 0 8px; font-size: 1.12rem; line-height: 1.4; letter-spacing: -.025em; }}
.project-description {{ margin: 0; color: var(--muted); font-size: .92rem; }}
.project-tech-list {{ display: flex; flex-wrap: wrap; gap: 7px; margin-top: 17px; }}
.project-tech {{
  padding: 4px 8px;
  border-radius: 6px;
  background: #f0f2f8;
  color: #4d5870;
  font-size: .76rem;
  font-weight: 650;
}}
.project-actions {{ display: flex; flex-wrap: wrap; gap: 13px; margin-top: auto; padding-top: 20px; }}
.project-action {{ font-size: .84rem; font-weight: 750; text-decoration: none; }}
.project-action:hover {{ text-decoration: underline; }}
.secondary-action {{ color: var(--muted); }}
.text-link {{ color: var(--accent); }}
footer {{
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  padding: 25px 6px 10px;
  color: var(--muted);
  font-size: .82rem;
}}
footer a {{ font-weight: 700; text-decoration: none; }}
@media (max-width: 680px) {{
  .container {{ width: calc(100% - 24px); margin: 12px auto; }}
  .site-nav {{ align-items: flex-start; flex-direction: column; gap: 10px; }}
  .nav-links {{ justify-content: flex-start; gap: 8px 15px; }}
  .hero {{ padding: 32px 23px; border-radius: 22px; }}
  .hero-bottom {{ align-items: flex-start; flex-direction: column; }}
  .section {{ padding: 24px 20px; border-radius: 16px; }}
  .project-grid {{ grid-template-columns: 1fr; }}
  .entry-heading {{ align-items: flex-start; flex-direction: column; gap: 2px; }}
  footer {{ flex-direction: column; }}
}}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{
    scroll-behavior: auto !important;
    transition-duration: .01ms !important;
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
  }}
}}
@media print {{
  @page {{ margin: 14mm; }}
  body {{ background: #fff; }}
  .container {{ width: 100%; margin: 0; }}
  .site-nav {{ display: none; }}
  .hero, .section {{ box-shadow: none; break-inside: avoid; }}
  .project-card {{ break-inside: avoid; }}
  .project-card:hover {{ transform: none; }}
  a {{ color: inherit; }}
  footer {{ padding-top: 15px; }}
}}
</style>
</head>
<body>
<main class="container">
  <nav class="site-nav" aria-label="Main navigation">
    <a class="brand" href="#top">{name}</a>
    <div class="nav-links">{navigation}</div>
  </nav>

  <header class="hero" id="top">
    <p class="eyebrow">Personal portfolio</p>
    <h1>{name}</h1>
    {f'<p class="headline">{headline}</p>' if headline else ""}
    {f'<p class="hero-summary">{summary}</p>' if summary else ""}
    <div class="hero-bottom">
      <div class="contact">{contact_html}</div>
      {f'<div class="social-links">{social_html}</div>' if social_html else ""}
    </div>
  </header>

  {about_html}
  {"".join(sections)}

  <footer>
    <span>© {name} · Personal portfolio</span>
    {footer_contact}
  </footer>
</main>
</body>
</html>"""


def save_portfolio_html(profile, output_path):
    """Generate and save the portfolio HTML; return the output Path."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    html = generate_portfolio_html(profile)
    output_path.write_text(html, encoding="utf-8")
    return output_path
