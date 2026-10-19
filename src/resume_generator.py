
"""Professional, ATS-friendly PDF resume generator for CareerForge AI."""

from io import BytesIO
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    KeepTogether,
    PageBreak,
)


# Professional, print-friendly color palette
NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#285A7A")
DARK = colors.HexColor("#252B33")
MUTED = colors.HexColor("#5D6875")
LIGHT = colors.HexColor("#D9E1E8")


def _text(value):
    """Convert values safely to readable text."""
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return ", ".join(filter(None, (_text(item) for item in value)))
    if isinstance(value, dict):
        return _text(
            value.get("text")
            or value.get("description")
            or value.get("name")
            or ""
        )
    return str(value).strip()


def _first(data, *keys, default=""):
    """Return the first non-empty value from a dictionary."""
    if not isinstance(data, dict):
        return default

    for key in keys:
        value = data.get(key)
        if value is not None and value != "":
            return value

    return default


def _safe(value):
    """Escape user-provided text for ReportLab Paragraph markup."""
    text = escape(_text(value))
    # Preserve ordinary line breaks as paragraph spacing.
    return text.replace("\n", "<br/>")


def _clean_url(value):
    """Normalize a URL for display without inventing a destination."""
    url = _text(value)
    if not url:
        return ""

    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", url):
        return url

    if "@" in url and " " not in url:
        return url

    if "." in url and " " not in url:
        return "https://" + url

    return url


def _items(value):
    """Normalize optional section data to a list."""
    if value is None or value == "":
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    if isinstance(value, dict):
        return [value]

    if isinstance(value, str):
        return [line.strip(" •-\t") for line in value.splitlines() if line.strip()]

    return [value]


def _bullets(value):
    """Normalize descriptions or achievements to a list of bullet points."""
    if value is None or value == "":
        return []

    if isinstance(value, (list, tuple)):
        result = []
        for item in value:
            if isinstance(item, dict):
                item = _first(
                    item, "text", "description", "achievement", "bullet",
                    default=""
                )
            text = _text(item).strip(" •-\t")
            if text:
                result.append(text)
        return result

    text = _text(value)
    if not text:
        return []

    lines = re.split(r"\n+|(?<=[.!?])\s+(?=[A-Z0-9])", text)
    return [line.strip(" •-\t") for line in lines if line.strip(" •-\t")]


def _link(label, value):
    """Build a readable contact detail without a decorative icon."""
    value = _text(value)
    if not value:
        return ""

    return f"<b>{_safe(label)}:</b> {_safe(value)}"


def _styles():
    """Create consistent resume typography."""
    base = getSampleStyleSheet()

    return {
        "name": ParagraphStyle(
            "ResumeName",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=23,
            leading=27,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "headline": ParagraphStyle(
            "ResumeHeadline",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=BLUE,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "contact": ParagraphStyle(
            "ResumeContact",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=5,
            wordWrap="CJK",
        ),
        "section": ParagraphStyle(
            "ResumeSection",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=14,
            textColor=NAVY,
            spaceBefore=9,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "ResumeBody",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12.5,
            textColor=DARK,
            spaceAfter=3,
            splitLongWords=1,
            wordWrap="CJK",
        ),
        "item_title": ParagraphStyle(
            "ResumeItemTitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.2,
            leading=12,
            textColor=DARK,
            spaceBefore=3,
            spaceAfter=1,
            keepWithNext=True,
        ),
        "meta": ParagraphStyle(
            "ResumeMeta",
            parent=base["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8.3,
            leading=11,
            textColor=MUTED,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "bullet": ParagraphStyle(
            "ResumeBullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=12,
            leftIndent=11,
            firstLineIndent=-8,
            bulletIndent=0,
            textColor=DARK,
            spaceAfter=2,
            splitLongWords=1,
            wordWrap="CJK",
        ),
    }


def _section(title, styles, story):
    """Add a clearly separated section heading."""
    story.append(Paragraph(_safe(title.upper()), styles["section"]))
    story.append(
        HRFlowable(
            width="100%",
            thickness=0.7,
            color=LIGHT,
            spaceBefore=0,
            spaceAfter=5,
        )
    )


def _add_bullets(values, styles, story):
    """Append plain, ATS-friendly bullet paragraphs."""
    for item in _bullets(values):
        story.append(Paragraph("&#8226; " + _safe(item), styles["bullet"]))


def _add_experience(profile, styles, story):
    experience = _items(
        _first(profile, "experience", "work_experience", "employment", default=[])
    )
    if not experience:
        return

    _section("Work Experience", styles, story)

    for job in experience:
        if not isinstance(job, dict):
            story.append(Paragraph(_safe(job), styles["body"]))
            continue

        title = _first(
            job, "title", "role", "position", "job_title", default=""
        )
        company = _first(
            job, "company", "employer", "organization", default=""
        )
        dates = _first(
            job, "duration", "dates", "date_range", "period", default=""
        )
        start = _first(job, "start_date", "start", default="")
        end = _first(job, "end_date", "end", default="")
        if not dates:
            dates = " – ".join(filter(None, [_text(start), _text(end)]))

        heading = " | ".join(filter(None, [_text(title), _text(company)]))
        if heading:
            story.append(Paragraph(_safe(heading), styles["item_title"]))

        location = _first(job, "location", "place", default="")
        meta = " | ".join(filter(None, [_text(dates), _text(location)]))
        if meta:
            story.append(Paragraph(_safe(meta), styles["meta"]))

        description = _first(
            job, "achievements", "bullets", "responsibilities",
            "description", "highlights", default=[]
        )
        _add_bullets(description, styles, story)


def _add_education(profile, styles, story):
    education = _items(
        _first(profile, "education", "academic_background", default=[])
    )
    if not education:
        return

    _section("Education", styles, story)

    for item in education:
        if not isinstance(item, dict):
            story.append(Paragraph(_safe(item), styles["body"]))
            continue

        degree = _first(
            item, "degree", "qualification", "program", "course", default=""
        )
        institution = _first(
            item, "institution", "school", "university", "college", default=""
        )
        heading = " | ".join(
            filter(None, [_text(degree), _text(institution)])
        )
        if heading:
            story.append(Paragraph(_safe(heading), styles["item_title"]))

        dates = _first(item, "duration", "dates", "year", "graduation_year", default="")
        start = _first(item, "start_date", default="")
        end = _first(item, "end_date", default="")
        if not dates:
            dates = " – ".join(filter(None, [_text(start), _text(end)]))

        details = _first(item, "details", "grade", "gpa", default="")
        meta = " | ".join(filter(None, [_text(dates), _text(details)]))
        if meta:
            story.append(Paragraph(_safe(meta), styles["meta"]))


def _add_projects(profile, styles, story):
    projects = _items(_first(profile, "projects", "personal_projects", default=[]))
    if not projects:
        return

    _section("Projects", styles, story)

    for project in projects:
        if not isinstance(project, dict):
            story.append(Paragraph(_safe(project), styles["body"]))
            continue

        name = _first(project, "name", "title", "project_name", default="")
        technologies = _first(
            project, "technologies", "tech_stack", "tools", default=""
        )
        url = _first(project, "url", "link", "github", default="")

        heading = _text(name)
        if heading:
            story.append(Paragraph(_safe(heading), styles["item_title"]))

        meta = " | ".join(
            filter(None, [_text(technologies), _text(url)])
        )
        if meta:
            story.append(Paragraph(_safe(meta), styles["meta"]))

        description = _first(
            project, "bullets", "highlights", "description",
            "achievements", default=[]
        )
        _add_bullets(description, styles, story)


def _add_certifications(profile, styles, story):
    certifications = _items(
        _first(profile, "certifications", "certificates", "licenses", default=[])
    )
    if not certifications:
        return

    _section("Certifications", styles, story)

    for cert in certifications:
        if isinstance(cert, dict):
            name = _first(cert, "name", "title", "certification", default="")
            issuer = _first(cert, "issuer", "organization", "provider", default="")
            year = _first(cert, "year", "date", "issued", default="")
            line = " | ".join(
                filter(None, [_text(name), _text(issuer), _text(year)])
            )
        else:
            line = _text(cert)

        if line:
            story.append(Paragraph("&#8226; " + _safe(line), styles["bullet"]))


def _add_skills(profile, styles, story):
    skills = _first(
        profile, "skills", "technical_skills", "core_skills", default=[]
    )
    if not skills:
        return

    if isinstance(skills, dict):
        _section("Skills", styles, story)
        for category, values in skills.items():
            values_text = _text(values)
            if values_text:
                story.append(
                    Paragraph(
                        f"<b>{_safe(category)}:</b> {_safe(values_text)}",
                        styles["body"],
                    )
                )
        return

    skills_list = _items(skills)
    skills_text = ", ".join(
        _text(skill) for skill in skills_list if _text(skill)
    )
    if skills_text:
        _section("Skills", styles, story)
        story.append(Paragraph(_safe(skills_text), styles["body"]))


def _add_languages(profile, styles, story):
    languages = _first(profile, "languages", "spoken_languages", default=[])
    languages_text = _text(languages)
    if languages_text:
        _section("Languages", styles, story)
        story.append(Paragraph(_safe(languages_text), styles["body"]))


def _add_footer(canvas, doc):
    """Add a subtle page number without interfering with resume content."""
    canvas.saveState()
    canvas.setStrokeColor(LIGHT)
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, 14 * mm, A4[0] - 20 * mm, 14 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(
        A4[0] - 20 * mm,
        9 * mm,
        f"Page {doc.page}",
    )
    canvas.restoreState()


def generate_resume_pdf(profile):
    """
    Generate a professional resume PDF from a profile dictionary.

    Args:
        profile (dict): Resume information. Common keys include:
            name, email, phone, location, linkedin, github, website,
            headline, summary, skills, experience, education, projects,
            certifications, and languages.

    Returns:
        bytes: PDF bytes, suitable for Streamlit's download_button.
    """
    if not isinstance(profile, dict):
        raise TypeError("profile must be a dictionary.")

    styles = _styles()
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=15 * mm,
        bottomMargin=19 * mm,
        title=f"Resume - {_text(profile.get('name')) or 'Candidate'}",
        author="CareerForge AI",
        subject="Professional Resume",
        pageCompression=1,
    )

    story = []

    # Header
    name = _first(profile, "name", "full_name", "candidate_name", default="Your Name")
    story.append(Paragraph(_safe(name), styles["name"]))

    headline = _first(
        profile, "headline", "professional_title", "job_title", "title", default=""
    )
    if headline:
        story.append(Paragraph(_safe(headline), styles["headline"]))

    contact_keys = [
        ("Email", _first(profile, "email", "email_address", default="")),
        ("Phone", _first(profile, "phone", "phone_number", "mobile", default="")),
        ("Location", _first(profile, "location", "city", "address", default="")),
        ("LinkedIn", _clean_url(_first(profile, "linkedin", "linkedin_url", default=""))),
        ("GitHub", _clean_url(_first(profile, "github", "github_url", default=""))),
        ("Website", _clean_url(_first(profile, "website", "portfolio", "website_url", default=""))),
    ]

    contact_lines = []
    current_line = []

    for label, value in contact_keys:
        if value:
            current_line.append(_link(label, value))

    # Keep contact information readable, including when there are many links.
    if current_line:
        contact_lines = [
            "  |  ".join(current_line[index:index + 3])
            for index in range(0, len(current_line), 3)
        ]

    for line in contact_lines:
        story.append(Paragraph(line, styles["contact"]))

    story.append(Spacer(1, 4))
    story.append(
        HRFlowable(
            width="100%",
            thickness=1.2,
            color=BLUE,
            spaceBefore=2,
            spaceAfter=5,
        )
    )

    # Summary
    summary = _first(
        profile,
        "summary",
        "professional_summary",
        "objective",
        "profile",
        "about",
        default="",
    )
    if summary:
        _section("Professional Summary", styles, story)
        story.append(Paragraph(_safe(summary), styles["body"]))

    # Core sections
    _add_skills(profile, styles, story)
    _add_experience(profile, styles, story)
    _add_projects(profile, styles, story)
    _add_education(profile, styles, story)
    _add_certifications(profile, styles, story)
    _add_languages(profile, styles, story)

    if not any(
        _first(profile, key, default="")
        for key in (
            "summary", "professional_summary", "objective", "profile", "about",
            "skills", "technical_skills", "core_skills", "experience",
            "work_experience", "employment", "projects", "personal_projects",
            "education", "academic_background", "certifications", "certificates",
            "languages", "spoken_languages",
        )
    ):
        story.append(
            Paragraph(
                "Add your professional summary, skills, work experience, "
                "education, or projects to create a complete resume.",
                styles["body"],
            )
        )

    doc.build(
        story,
        onFirstPage=_add_footer,
        onLaterPages=_add_footer,
    )

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
