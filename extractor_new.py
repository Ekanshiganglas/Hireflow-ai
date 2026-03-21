# extractor.py
import re

SKILLS_LIST = [
    "python", "java", "javascript", "c++", "c#", "php", "ruby", "swift",
    "kotlin", "go", "rust", "typescript", "r", "matlab", "scala",
    "html", "css", "react", "angular", "vue", "nodejs", "node.js",
    "django", "flask", "fastapi", "express", "spring", "asp.net",
    "sql", "mysql", "postgresql", "mongodb", "redis", "oracle",
    "sqlite", "cassandra", "dynamodb",
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
    "jenkins", "git", "github", "gitlab", "ci/cd", "terraform",
    "machine learning", "deep learning", "data analysis", "data science",
    "artificial intelligence", "ai", "ml", "nlp", "computer vision",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras",
    "excel", "power bi", "tableau", "jira", "agile", "scrum",
    "rest api", "graphql", "microservices", "linux", "windows",
    "leadership", "communication", "teamwork", "problem solving",
    "project management", "analytical thinking"
]

def extract_email(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(pattern, text)
    return matches[0] if matches else "Not found"

def extract_phone(text):
    pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)(\d{3}[-.\s]?\d{4})'
    matches = re.findall(pattern, text)
    if matches:
        phone = ''.join(matches[0])
        return phone
    else:
        return "Not found"

def extract_skills(text):
    text_lower = text.lower()
    found_skills = []
    for skill in SKILLS_LIST:
        if skill in text_lower:
            found_skills.append(skill)
    return list(set(found_skills))

def extract_name(text):
    lines = text.strip().split('\n')
    if lines:
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) < 50 and not any(char.isdigit() for char in line):
                skip_words = ['resume', 'curriculum', 'vitae', 'cv', 'profile', 'summary', 'objective', 'contact', 'email', 'phone', 'address']
                if not any(skip in line.lower() for skip in skip_words):
                    return line
    return "Not found"

def extract_all(text):
    extracted_info = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
    }
    return extracted_info