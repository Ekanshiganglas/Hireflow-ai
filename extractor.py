# extractor.py
# This file extracts specific information from resume text

import re

# Make spaCy optional for deployment
try:
    import spacy
    nlp = None
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    nlp = None

# List of common skills to look for in resumes
SKILLS_LIST = [
    # Programming Languages
    "python", "java", "javascript", "c++", "c#", "php", "ruby", "swift",
    "kotlin", "go", "rust", "typescript", "r", "matlab", "scala",
    
    # Web Technologies
    "html", "css", "react", "angular", "vue", "nodejs", "node.js",
    "django", "flask", "fastapi", "express", "spring", "asp.net",
    
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "oracle",
    "sqlite", "cassandra", "dynamodb",
    
    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
    "jenkins", "git", "github", "gitlab", "ci/cd", "terraform",
    
    # Data Science & ML
    "machine learning", "deep learning", "data analysis", "data science",
    "artificial intelligence", "ai", "ml", "nlp", "computer vision",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras",
    
    # Tools & Other
    "excel", "power bi", "tableau", "jira", "agile", "scrum",
    "rest api", "graphql", "microservices", "linux", "windows",
    
    # Soft Skills
    "leadership", "communication", "teamwork", "problem solving",
    "project management", "analytical thinking"
]


def extract_email(text):
    """
    Finds email addresses in text using pattern matching.
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(pattern, text)
    return matches[0] if matches else "Not found"


def extract_phone(text):
    """
    Finds phone numbers in text.
    """
    pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)(\d{3}[-.\s]?\d{4})'
    matches = re.findall(pattern, text)
    
    if matches:
        phone = ''.join(matches[0])
        return phone
    else:
        return "Not found"


def extract_skills(text):
    """
    Identifies which skills from our skills list appear in the resume.
    """
    text_lower = text.lower()
    found_skills = []
    
    for skill in SKILLS_LIST:
        if skill in text_lower:
            found_skills.append(skill)
    
    return list(set(found_skills))


def extract_name(text):
    """
    Attempts to extract the person's name from the resume.
    """
    lines = text.strip().split('\n')
    
    if lines:
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) < 50 and not any(char.isdigit() for char in line):
                skip_words = ['resume', 'curriculum', 'vitae', 'cv', 'profile', 'summary', 
                             'objective', 'contact', 'email', 'phone', 'address']
                if not any(skip in line.lower() for skip in skip_words):
                    return line
    
    return "Not found"


def extract_all(text):
    """
    Extracts all information from resume text.
    """
    extracted_info = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
    }
    
    return extracted_info
 - remove syntax error
