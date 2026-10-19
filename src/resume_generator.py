from html import escape
from io import BytesIO
from xml.sax.saxutils import quoteattr

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    KeepTogether,
)


def _plain(value):
    """Convert a value to readable plain text."""
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return ", ".join(_plain(item) for item in value if item is not None)
    if isinstance(value, dict):
        return "; ".join(
            f"{_plain(key)}: {_plain(item)}"
            for key, item in value.items()
            if item is not None
        )
    return str(value).strip()


def _paragraph_text(value):
    """Escape user content before placing it inside a ReportLab paragraph."""
    return escape(_plain(value)).replace("\n", "<br/>")


def _items(value):
    if value is None:
        return []
    if isinstance(value, str):
        return [line.strip() for line in value.splitlines() if line.strip()]
    if isinstance(value, dict):
        return [value]
    try:
        return list(value)
    except TypeError:
        return [value]


def _field(item, *keys):
    if not isinstance(item, dict):
        return ""
    for key in keys:
        value = item.get(key)
        if value:
            return _plain(value)
    return ""


def generate_resume_pdf(profile):
    """Generate a clean, single-column resume PDF and return its bytes."""
    profile = profile or {}
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
        title=f"{_plain(profile.get('name')) or 'Resume'} - Resume",
        author=_plain(profile.get("name")) or "Resume Generator",
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="ResumeName",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=25,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#172033"),
        spaceAfter=5,
    ))
    styles.add(ParagraphStyle(
        name="ResumeContact",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#444B59"),
        spaceAfter=7,
    ))
    styles.add(ParagraphStyle(
        name="ResumeSection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#243B63"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    ))
    styles.add(ParagraphStyle(
        name="ResumeBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=12,
        spaceAfter=3,
        textColor=colors.HexColor("#20242C"),
    ))
    styles.add(ParagraphStyle(
        name="ResumeEntry",
        parent=styles["BodyText"],
        fontSize=9,
        leading=12,
        spaceBefore=2,
        spaceAfter=2,
        textColor=colors.HexColor("#20242C"),
    ))

    story = []

    name = _plain(profile.get("name")) or "Your Name"
    story.append(Paragraph(_paragraph_text(name), styles["ResumeName"]))

    contact = []
    for key in ("email", "phone", "location"):
        value = _plain(profile.get(key))
        if value:
            contact.append(_paragraph_text(value))

    # Only add clickable links for ordinary web URLs and email addresses.
    email = _plain(profile.get("email"))
    if email and "@" in email and not any(c in email for c in '<>"'):
        email_link = (
            f'<link href={quoteattr("mailto:" + email)}>'
            f'{_paragraph_text(email)}</link>'
        )
        contact = [
            part for part in contact
            if part != _paragraph_text(email)
        ]
        contact.insert(0, email_link)

    for key, label in (("linkedin", "LinkedIn"), ("website", "Website")):
        url = _plain(profile.get(key))
        if url.startswith(("https://", "http://")):
            contact.append(
                f'<link href={quoteattr(url)}>{label}</link>'
            )

    if contact:
        story.append(Paragraph(" | ".join(contact), styles["ResumeContact"]))

    story.append(HRFlowable(
        width="100%",
        thickness=0.8,
        color=colors.HexColor("#CBD3E1"),
        spaceAfter=5,
    ))

    def add_section(title, content):
        if not content:
            return
        story.append(Paragraph(escape(title.upper()), styles["ResumeSection"]))
        story.append(HRFlowable(
            width="100%",
            thickness=0.4,
            color=colors.HexColor("#D7DDE7"),
            spaceAfter=5,
        ))
        story.extend(content)

    summary = _plain(profile.get("summary"))
    if summary:
        add_section("Professional Summary", [
            Paragraph(_paragraph_text(summary), styles["ResumeBody"])
        ])

    skills = _items(profile.get("skills"))
    if skills:
        skill_text = "  •  ".join(
            _paragraph_text(skill) for skill in skills if _plain(skill)
        )
        add_section("Skills", [
            Paragraph(skill_text, styles["ResumeBody"])
        ])

    experience_content = []
    for item in _items(profile.get("experience")):
        if isinstance(item, dict):
            role = _field(item, "title", "role", "position")
            company = _field(item, "company", "employer")
            dates = _field(item, "dates", "duration", "period")
            description = _field(item, "description", "details", "responsibilities")
            heading = " — ".join(x for x in (role, company) if x)
            if dates:
                heading = f"{heading} | {dates}" if heading else dates
            if heading:
                experience_content.append(
                    Paragraph(_paragraph_text(heading), styles["ResumeEntry"])
                )
            if description:
                experience_content.append(
                    Paragraph(_paragraph_text(description), styles["ResumeBody"])
                )
        else:
            text = _plain(item)
            if text:
                experience_content.append(
                    Paragraph(_paragraph_text(text), styles["ResumeBody"])
                )

    add_section("Experience", experience_content)

    projects_content = []
    for item in _items(profile.get("projects")):
        if isinstance(item, dict):
            title = _field(item, "name", "title", "project")
            description = _field(item, "description", "details")
            technologies = _field(item, "technologies", "tech", "skills")
            link = _field(item, "link", "url")

            if title:
                projects_content.append(
                    Paragraph(_paragraph_text(title), styles["ResumeEntry"])
                )
            if description:
                projects_content.append(
                    Paragraph(_paragraph_text(description), styles["ResumeBody"])
                )
            if technologies:
                projects_content.append(
                    Paragraph(
                        "<i>Technologies:</i> " + _paragraph_text(technologies),
                        styles["ResumeBody"],
                    )
                )
            if link.startswith(("https://", "http://")):
                projects_content.append(
                    Paragraph(
                        f'<link href={quoteattr(link)}>{_paragraph_text(link)}</link>',
                        styles["ResumeBody"],
                    )
                )
        else:
            text = _plain(item)
            if text:
                projects_content.append(
                    Paragraph(_paragraph_text(text), styles["ResumeBody"])
                )

    add_section("Projects", projects_content)

    education_content = []
    for item in _items(profile.get("education")):
        if isinstance(item, dict):
            degree = _field(item, "degree", "title", "qualification")
            institution = _field(item, "institution", "school", "college")
            dates = _field(item, "dates", "year", "duration")
            details = _field(item, "description", "details")
            heading = " — ".join(x for x in (degree, institution) if x)
            if dates:
                heading = f"{heading} | {dates}" if heading else dates
            if heading:
                education_content.append(
                    Paragraph(_paragraph_text(heading), styles["ResumeEntry"])
                )
            if details:
                education_content.append(
                    Paragraph(_paragraph_text(details), styles["ResumeBody"])
                )
        else:
            text = _plain(item)
            if text:
                education_content.append(
                    Paragraph(_paragraph_text(text), styles["ResumeBody"])
                )

    add_section("Education", education_content)

    if len(story) <= 3:
        story.append(Paragraph(
            "Add your summary, skills, experience, projects, or education "
            "to build a more complete resume.",
            styles["ResumeBody"],
        ))

    document.build(story)
    return buffer.getvalue()
