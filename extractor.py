# extractor.py
# This file extracts specific information from resume text

import re
import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

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
    
    Args:
        text: The resume text
    
    Returns:
        Email address as a string, or "Not found"
    """
    # Pattern that matches email format: something@something.com
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Find all matches
    matches = re.findall(pattern, text)
    
    # Return the first email found, or "Not found"
    return matches[0] if matches else "Not found"


def extract_phone(text):
    """
    Finds phone numbers in text.
    
    Args:
        text: The resume text
    
    Returns:
        Phone number as a string, or "Not found"
    """
    # Pattern that matches various phone formats
    # Examples: (123) 456-7890, 123-456-7890, +91 1234567890
    pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)(\d{3}[-.\s]?\d{4})'
    
    # Find all matches
    matches = re.findall(pattern, text)
    
    if matches:
        # Join the parts of the first match
        phone = ''.join(matches[0])
        return phone
    else:
        return "Not found"


def extract_skills(text):
    """
    Identifies which skills from our skills list appear in the resume.
    
    Args:
        text: The resume text
    
    Returns:
        List of skills found
    """
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Find which skills from our list appear in the text
    found_skills = []
    for skill in SKILLS_LIST:
        if skill in text_lower:
            found_skills.append(skill)
    
    # Remove duplicates and return
    return list(set(found_skills))


def extract_name(text):
    """
    Attempts to extract the person's name from the resume.
    This is tricky! We'll use a simple approach.
    
    Args:
        text: The resume text
    
    Returns:
        Name as a string, or "Not found"
    """
    # Process text with spaCy to find named entities
    doc = nlp(text[:500])  # Only check first 500 characters (where name usually is)
    
    # Look for PERSON entities (spaCy identifies people's names)
    for entity in doc.ents:
        if entity.label_ == "PERSON":
            return entity.text
    
    return "Not found"


def extract_all(text):
    """
    Extracts all information from resume text.
    
    Args:
        text: The complete resume text
    
    Returns:
        Dictionary with all extracted information
    """
    print("Extracting information from resume...")
    
    extracted_info = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
    }
    
    return extracted_info


# Test code - runs when you execute this file directly
if __name__ == "__main__":
    # Import parser to read the resume
    from parser import extract_text
    
    print("Reading resume file...")
    resume_text = extract_text("sample_resume.docx")
    
    print("\n" + "="*50)
    print("EXTRACTING INFORMATION")
    print("="*50 + "\n")
    
    # Extract all information
    info = extract_all(resume_text)
    
    # Display results
    print("\n" + "="*50)
    print("EXTRACTED INFORMATION")
    print("="*50 + "\n")
    
    print(f"👤 Name: {info['name']}")
    print(f"📧 Email: {info['email']}")
    print(f"📱 Phone: {info['phone']}")
    print(f"\n💼 Skills Found ({len(info['skills'])} total):")
    
    if info['skills']:
        # Print skills in a nice format, 5 per line
        for i in range(0, len(info['skills']), 5):
            skills_row = info['skills'][i:i+5]
            print("   • " + ", ".join(skills_row))
    else:
        print("   No skills detected")
    
    print("\n" + "="*50)
    print("✅ Extraction complete!")
    print("="*50)
