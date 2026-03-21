# suggester.py
# Free Resume Suggestion Engine (No API Required)

def get_resume_suggestions(resume_text, job_description, match_score, matched_skills, missing_skills):
    """
    Generates intelligent resume improvement suggestions
    without using any external API.
    """

    suggestions = []

    # =====================================================
    # 1. Overall Assessment
    # =====================================================
    if match_score >= 75:
        assessment = (
            "Strong alignment with the job requirements. "
            "The candidate demonstrates solid technical compatibility and relevant experience."
        )
    elif match_score >= 50:
        assessment = (
            "Moderate alignment with the job description. "
            "Some important skills are present, but improvements are needed."
        )
    else:
        assessment = (
            "Low alignment with the job description. "
            "Several key skills and experiences are missing."
        )

    suggestions.append("========== OVERALL ASSESSMENT ==========")
    suggestions.append(assessment)

    # =====================================================
    # 2. Key Strengths
    # =====================================================
    suggestions.append("\n========== KEY STRENGTHS ==========")

    if matched_skills:
        for skill in matched_skills[:5]:
            suggestions.append(f"• Demonstrated experience in {skill}")
    else:
        suggestions.append("• No strong skill matches identified.")

    # =====================================================
    # 3. Areas for Improvement
    # =====================================================
    suggestions.append("\n========== AREAS FOR IMPROVEMENT ==========")

    if missing_skills:
        for skill in missing_skills:
            suggestions.append(f"• Consider adding practical experience with {skill}")
    else:
        suggestions.append("• Resume already covers most required skills.")

    # =====================================================
    # 4. Specific Recommendations
    # =====================================================
    suggestions.append("\n========== SPECIFIC RECOMMENDATIONS ==========")

    suggestions.append("• Add measurable achievements (e.g., improved efficiency by 30%).")
    suggestions.append("• Include more technical details about your projects.")
    suggestions.append("• Align resume keywords exactly with job description keywords.")
    suggestions.append("• Highlight frameworks, tools, and technologies clearly.")
    suggestions.append("• Add GitHub, portfolio, or live project links.")

    # =====================================================
    # 5. Resume Rewrite Suggestions
    # =====================================================
    suggestions.append("\n========== RESUME REWRITE SUGGESTIONS ==========")

    suggestions.append("\nBefore: Worked on a web development project.")
    suggestions.append(
        "After: Developed a scalable web application using Python and Flask, "
        "reducing server response time by 40% and improving user experience."
    )

    suggestions.append("\nBefore: Responsible for database management.")
    suggestions.append(
        "After: Designed and optimized SQL database schemas, "
        "improving query performance by 35%."
    )

    return "\n".join(suggestions)


# ==============================
# Test Mode
# ==============================
if __name__ == "__main__":
    from parser import extract_text
    from scorer import calculate_match_score, get_matching_keywords

    print("\n" + "="*60)
    print("AI-POWERED RESUME SUGGESTIONS ")
    print("="*60 + "\n")

    print("📄 Reading resume...")
    resume_text = extract_text("sample_resume.docx")

    job_description = """
    Senior Python Developer

    Required Skills:
    - 5+ years Python development experience
    - Django or Flask framework
    - React or Vue.js frontend
    - SQL databases
    - Git, Docker, AWS
    - REST API development
    - Machine learning (nice to have)
    """

    print("📊 Calculating match score...")
    score = calculate_match_score(resume_text, job_description)
    keywords = get_matching_keywords(resume_text, job_description)

    print(f"Match Score: {score}%")
    print(f"Matched: {len(keywords['matched'])} skills")
    print(f"Missing: {len(keywords['missing'])} skills")

    print("\n🤖 Generating AI suggestions...\n")

    suggestions = get_resume_suggestions(
        resume_text,
        job_description,
        score,
        keywords['matched'],
        keywords['missing']
    )

    print("="*60)
    print(suggestions)
    print("="*60)

    print("\n✅ Suggestions generated successfully!")