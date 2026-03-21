# scorer.py
# This file compares a resume with a job description and gives a match score

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_score(resume_text, job_description):
    """
    Compares resume text with job description and calculates similarity.
    
    How it works:
    1. Converts both texts into numerical vectors (lists of numbers)
    2. Uses TF-IDF (Term Frequency-Inverse Document Frequency) algorithm
    3. Calculates cosine similarity (mathematical measure of similarity)
    4. Returns a percentage score
    
    Args:
        resume_text: The complete text from the resume
        job_description: The job posting text
    
    Returns:
        A score from 0 to 100 (percentage match)
    """
    
    # TF-IDF Vectorizer converts text to numbers
    # It measures how important each word is
    vectorizer = TfidfVectorizer()
    
    # Combine both texts so the vectorizer learns all words
    documents = [resume_text, job_description]
    
    # Convert texts to numerical vectors
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Calculate cosine similarity
    # This measures the angle between two vectors
    # Result: 0.0 (completely different) to 1.0 (identical)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # Convert to percentage (0-100)
    score = round(similarity * 100, 2)
    
    return score


def get_matching_keywords(resume_text, job_description):
    """
    Finds which important keywords from the job description appear in the resume.
    
    Args:
        resume_text: The complete resume text
        job_description: The job posting text
    
    Returns:
        Dictionary with matched and missing keywords
    """
    
    # Convert to lowercase for comparison
    resume_lower = resume_text.lower()
    job_lower = job_description.lower()
    
    # Common important keywords to look for
    important_keywords = [
        "python", "java", "javascript", "react", "angular", "vue",
        "django", "flask", "spring", "nodejs", "sql", "nosql",
        "aws", "azure", "docker", "kubernetes", "git", "agile",
        "machine learning", "data analysis", "api", "microservices",
        "leadership", "communication", "teamwork", "problem solving"
    ]
    
    # Find which keywords are in the job description
    job_keywords = [kw for kw in important_keywords if kw in job_lower]
    
    # Check which of those are also in the resume
    matched = [kw for kw in job_keywords if kw in resume_lower]
    missing = [kw for kw in job_keywords if kw not in resume_lower]
    
    return {
        "matched": matched,
        "missing": missing,
        "match_count": len(matched),
        "total_required": len(job_keywords)
    }


# Test code - runs when you execute this file directly
if __name__ == "__main__":
    # Import our previous modules
    from parser import extract_text
    from extractor import extract_all
    
    print("\n" + "="*60)
    print("SMART RESUME ANALYZER - JOB MATCHING")
    print("="*60 + "\n")
    
    # Read the resume
    print("📄 Reading resume...")
    resume_text = extract_text("sample_resume.docx")
    
    # Extract information
    print("🔍 Extracting information...")
    info = extract_all(resume_text)
    
    # Sample job description (you can change this!)
    job_description = """
    Senior Software Developer
    
    We are looking for an experienced Senior Software Developer to join our team.
    
    Required Skills:
    - 3+ years of experience in Python development
    - Strong knowledge of Django or Flask frameworks
    - Experience with React or Angular for frontend
    - Proficiency in SQL databases (MySQL, PostgreSQL)
    - Experience with Git version control
    - Knowledge of Docker and containerization
    - Understanding of REST APIs and microservices
    - Experience with AWS or other cloud platforms
    
    Nice to Have:
    - Machine Learning experience
    - Leadership and team management skills
    - Agile/Scrum methodology experience
    
    Responsibilities:
    - Develop and maintain web applications
    - Write clean, maintainable code
    - Collaborate with cross-functional teams
    - Mentor junior developers
    - Participate in code reviews
    """
    
    print("\n" + "="*60)
    print("JOB DESCRIPTION")
    print("="*60)
    print(job_description)
    
    # Calculate match score
    print("\n" + "="*60)
    print("ANALYZING MATCH...")
    print("="*60 + "\n")
    
    score = calculate_match_score(resume_text, job_description)
    keywords = get_matching_keywords(resume_text, job_description)
    
    # Display results
    print("\n" + "="*60)
    print("MATCH RESULTS")
    print("="*60 + "\n")
    
    print(f"📊 Overall Match Score: {score}%")
    
    # Visual representation
    if score >= 70:
        print("✅ EXCELLENT MATCH! This candidate is highly qualified.")
        bar = "█" * 20
    elif score >= 50:
        print("⚠️  GOOD MATCH! Candidate meets most requirements.")
        bar = "█" * int(score / 5)
    else:
        print("❌ WEAK MATCH. Candidate may need additional skills.")
        bar = "█" * int(score / 5)
    
    print(f"\n[{bar}{'░' * (20 - len(bar))}] {score}%\n")
    
    print(f"🎯 Keywords Matched: {keywords['match_count']}/{keywords['total_required']}")
    
    if keywords['matched']:
        print(f"\n✅ Matching Skills:")
        for i in range(0, len(keywords['matched']), 4):
            skills_row = keywords['matched'][i:i+4]
            print("   • " + ", ".join(skills_row))
    
    if keywords['missing']:
        print(f"\n❌ Missing Skills:")
        for i in range(0, len(keywords['missing']), 4):
            skills_row = keywords['missing'][i:i+4]
            print("   • " + ", ".join(skills_row))
    
    print("\n" + "="*60)
    print("👤 CANDIDATE SUMMARY")
    print("="*60 + "\n")
    print(f"Name: {info['name']}")
    print(f"Email: {info['email']}")
    print(f"Phone: {info['phone']}")
    print(f"Total Skills: {len(info['skills'])}")
    
    print("\n" + "="*60)
    print("✅ Analysis Complete!")
    print("="*60 + "\n")
