import re
from collections import Counter


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for",
    "from", "has", "have", "in", "is", "it", "of", "on", "or",
    "our", "that", "the", "this", "to", "was", "were", "will",
    "with", "you", "your", "we", "they", "their", "using",
    "use", "used", "work", "working", "role", "job", "team",
    "candidate", "ability", "skills", "experience", "required",
    "preferred", "responsibilities", "requirements",
}


def tokenize(text):
    """Normalize text into useful, unique word tokens."""
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]*", str(text or "").lower())
    return {
        word.strip(".-")
        for word in words
        if len(word.strip(".-")) > 1
        and word.strip(".-") not in STOP_WORDS
    }


def _profile_text(profile):
    """Collect searchable profile content."""
    profile = profile or {}
    parts = []

    for key in ("summary", "skills", "experience", "education", "projects"):
        value = profile.get(key, "")
        if isinstance(value, dict):
            parts.extend(str(v) for v in value.values())
        elif isinstance(value, (list, tuple, set)):
            for item in value:
                if isinstance(item, dict):
                    parts.extend(str(v) for v in item.values())
                else:
                    parts.append(str(item))
        else:
            parts.append(str(value or ""))

    return " ".join(parts)


def analyze_job_match(profile, job_description):
    """
    Compare a profile with a job description using keyword overlap.

    This is a simple heuristic, not a true ATS score or a guarantee
    of how an employer's screening system will rank an application.
    """
    profile_words = tokenize(_profile_text(profile))
    job_words = tokenize(job_description)

    if not job_words:
        return {
            "match_percentage": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "suggestions": [
                "Paste a job description containing responsibilities and qualifications."
            ],
        }

    matched = sorted(profile_words & job_words)
    missing = sorted(job_words - profile_words)

    percentage = round(100 * len(matched) / len(job_words))

    suggestions = []
    if missing:
        suggestions.append(
            "Review the missing keywords and add relevant skills or experience "
            "only when they accurately describe your background."
        )
    if percentage < 40:
        suggestions.append(
            "Compare the role's main responsibilities with your summary, skills, "
            "and project descriptions."
        )
    elif percentage < 70:
        suggestions.append(
            "Tailor your resume bullets to clearly describe relevant work, "
            "projects, and measurable results."
        )
    else:
        suggestions.append(
            "Check that your resume gives concrete examples for the relevant "
            "skills rather than listing keywords alone."
        )

    return {
        "match_percentage": percentage,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "suggestions": suggestions,
    }
