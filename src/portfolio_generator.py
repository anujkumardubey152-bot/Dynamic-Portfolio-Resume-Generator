from html import escape
from pathlib import Path


def _text(value):
    """Safely convert a value to HTML text."""
    return escape(str(value or "").strip())


def _items(value):
    """Normalize a list-like profile field."""
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.splitlines() if item.strip()]
    if isinstance(value, dict):
        return [value]
    try:
        return list(value)
    except TypeError:
        return []


def _section(title, content):
    if not content:
        return ""
    return f'<section class="section"><h2>{title}</h2>{content}</section>'


def generate_portfolio_html(profile):
    """Generate a responsive, standalone HTML portfolio."""
    profile = profile or {}

    name = _text(profile.get("name")) or "Your Name"
    email = _text(profile.get("email"))
    phone = _text(profile.get("phone"))
    location = _text(profile.get("location"))
    summary = _text(profile.get("summary"))
    linkedin = _text(profile.get("linkedin"))
    website = _text(profile.get("website"))

    skills = _items(profile.get("skills"))
    experience = _items(profile.get("experience"))
    education = _items(profile.get("education"))
    projects = _items(profile.get("projects"))

    contact_parts = []
    if email:
        contact_parts.append(
            f'<a href="mailto:{email}">{email}</a>'
        )
    if phone:
        contact_parts.append(f"<span>{phone}</span>")
    if location:
        contact_parts.append(f"<span>{location}</span>")
    if linkedin:
        contact_parts.append(
            f'<a href="{linkedin}" target="_blank" '
            f'rel="noopener noreferrer">LinkedIn</a>'
        )
    if website:
        contact_parts.append(
            f'<a href="{website}" target="_blank" '
            f'rel="noopener noreferrer">Website</a>'
        )

    contact_html = " <span class='separator'>·</span> ".join(contact_parts)

    skills_html = "".join(
        f'<span class="skill">{_text(skill)}</span>'
        for skill in skills
        if str(skill).strip()
    )

    experience_html = ""
    for item in experience:
        if isinstance(item, dict):
            title = _text(item.get("title") or item.get("role") or "Experience")
            company = _text(item.get("company"))
            dates = _text(item.get("dates") or item.get("duration"))
            description = _text(item.get("description"))
        else:
            title = "Experience"
            company = ""
            dates = ""
            description = _text(item)

        heading = title
        if company:
            heading += f" — {company}"
        if dates:
            heading += f" <span class='muted'>| {dates}</span>"

        experience_html += (
            f'<article class="entry"><h3>{heading}</h3>'
            f'<p>{description}</p></article>'
        )

    education_html = ""
    for item in education:
        if isinstance(item, dict):
            title = _text(
                item.get("degree") or item.get("title") or "Education"
            )
            institution = _text(
                item.get("institution") or item.get("school")
            )
            dates = _text(item.get("dates") or item.get("year"))
            details = _text(item.get("description"))
        else:
            title = _text(item)
            institution = ""
            dates = ""
            details = ""

        heading = title
        if institution:
            heading += f" — {institution}"
        if dates:
            heading += f" <span class='muted'>| {dates}</span>"

        education_html += (
            f'<article class="entry"><h3>{heading}</h3>'
            f'<p>{details}</p></article>'
        )

    projects_html = ""
    for item in projects:
        if isinstance(item, dict):
            title = _text(item.get("name") or item.get("title") or "Project")
            description = _text(item.get("description"))
            link = _text(item.get("link") or item.get("url"))
            tech = _items(item.get("technologies") or item.get("tech"))
        else:
            title = "Project"
            description = _text(item)
            link = ""
            tech = []

        title_html = title
        if link:
            title_html = (
                f'<a href="{link}" target="_blank" '
                f'rel="noopener noreferrer">{title}</a>'
            )

        tech_html = ""
        if tech:
            tech_html = (
                '<p class="muted">Technologies: '
                + ", ".join(_text(t) for t in tech)
                + "</p>"
            )

        projects_html += (
            f'<article class="entry"><h3>{title_html}</h3>'
            f'<p>{description}</p>{tech_html}</article>'
        )

    summary_html = (
        f'<section class="section"><h2>About</h2><p>{summary}</p></section>'
        if summary else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} | Portfolio</title>
<style>
:root {{
  color-scheme: light;
  --ink: #172033;
  --muted: #5e687b;
  --accent: #4f46e5;
  --surface: #ffffff;
  --background: #f3f5fb;
  --border: #e2e7f0;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  background: var(--background);
  color: var(--ink);
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont,
               "Segoe UI", sans-serif;
  line-height: 1.65;
}}
.container {{
  width: min(900px, calc(100% - 32px));
  margin: 42px auto;
}}
.hero {{
  padding: 44px 36px;
  border-radius: 22px;
  background: var(--ink);
  color: white;
  box-shadow: 0 18px 45px rgba(23, 32, 51, .12);
}}
.eyebrow {{
  margin: 0 0 8px;
  color: #c7d2fe;
  text-transform: uppercase;
  letter-spacing: .14em;
  font-size: .78rem;
  font-weight: 700;
}}
h1 {{
  margin: 0;
  font-size: clamp(2rem, 6vw, 3.5rem);
  line-height: 1.15;
  overflow-wrap: anywhere;
}}
.hero p {{ color: #e5e7eb; }}
.contact {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px 12px;
  margin-top: 20px;
  font-size: .93rem;
}}
a {{ color: var(--accent); }}
.hero a {{ color: #c7d2fe; }}
.separator {{ color: #94a3b8; }}
.section {{
  margin-top: 22px;
  padding: 26px 30px;
  border: 1px solid var(--border);
  border-radius: 18px;
  background: var(--surface);
}}
.section h2 {{
  margin: 0 0 16px;
  font-size: 1.2rem;
  letter-spacing: -.02em;
}}
.section h2::after {{
  content: "";
  display: block;
  width: 42px;
  height: 3px;
  margin-top: 8px;
  border-radius: 3px;
  background: var(--accent);
}}
.skills {{ display: flex; flex-wrap: wrap; gap: 9px; }}
.skill {{
  padding: 6px 12px;
  border: 1px solid #dfe3ff;
  border-radius: 999px;
  background: #f0f1ff;
  color: #3730a3;
  font-size: .9rem;
}}
.entry + .entry {{
  margin-top: 20px;
  padding-top: 18px;
  border-top: 1px solid var(--border);
}}
.entry h3 {{ margin: 0 0 6px; font-size: 1rem; }}
.entry p {{ margin: 5px 0 0; }}
.muted {{ color: var(--muted); font-weight: 400; }}
footer {{
  padding: 24px 8px;
  text-align: center;
  color: var(--muted);
  font-size: .85rem;
}}
@media (max-width: 600px) {{
  .container {{ margin: 18px auto; width: calc(100% - 20px); }}
  .hero {{ padding: 30px 22px; border-radius: 16px; }}
  .section {{ padding: 22px 18px; }}
}}
@media print {{
  body {{ background: white; }}
  .container {{ width: 100%; margin: 0; }}
  .hero, .section {{ box-shadow: none; }}
}}
</style>
</head>
<body>
<main class="container">
  <header class="hero">
    <p class="eyebrow">Personal Portfolio</p>
    <h1>{name}</h1>
    {f"<p>{summary}</p>" if summary else ""}
    <div class="contact">{contact_html}</div>
  </header>
  {summary_html}
  {_section("Skills", f'<div class="skills">{skills_html}</div>' if skills_html else "")}
  {_section("Experience", experience_html)}
  {_section("Projects", projects_html)}
  {_section("Education", education_html)}
  <footer>Portfolio created with Dynamic Portfolio and Resume Generator</footer>
</main>
</body>
</html>"""


def save_portfolio_html(profile, output_path):
    """Save the generated portfolio HTML to a file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    html = generate_portfolio_html(profile)
    output_path.write_text(html, encoding="utf-8")
    return output_path
