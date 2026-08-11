import pdfplumber

# List of skills to detect
SKILLS = [
    "Python", "Java", "C", "C++", "HTML", "CSS", "JavaScript",
    "SQL", "MySQL", "MongoDB", "React", "Node.js",
    "Machine Learning", "AI", "Data Science",
    "AutoCAD", "Excel", "Microsoft Excel",
    "Communication", "Leadership", "Teamwork",
    "English", "Telugu"
]


def extract_text(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def analyze_resume(text):

    found_skills = []

    lower_text = text.lower()

    for skill in SKILLS:
        if skill.lower() in lower_text:
            found_skills.append(skill)

    ats_score = min(len(found_skills) * 10, 100)

    missing_skills = []

    for skill in SKILLS:
        if skill not in found_skills:
            missing_skills.append(skill)

    suggestions = []

    if ats_score < 40:
        suggestions.append("Add more technical skills.")
        suggestions.append("Include projects.")
        suggestions.append("Improve resume formatting.")

    elif ats_score < 70:
        suggestions.append("Add certifications.")
        suggestions.append("Include internship experience.")
        suggestions.append("Mention achievements.")

    else:
        suggestions.append("Excellent resume.")
        suggestions.append("Keep your resume updated.")
        suggestions.append("Customize your resume for each job.")

    interview_questions = [
        "Tell me about yourself.",
        "Explain one of your projects.",
        "What are your strengths?",
        "Why should we hire you?",
        "What are your career goals?"
    ]

    return {
        "score": ats_score,
        "skills": found_skills,
        "missing": missing_skills,
        "suggestions": suggestions,
        "questions": interview_questions
    }