"""
Multi-Factor Scoring Engine
Calculates fair scores across multiple dimensions
"""

from typing import Dict, List
import numpy as np
from embedding_model import SemanticMatcher

class ScoringWeights:
    """
    How much each factor matters
    Total = 100%
    """
    SKILLS = 0.40       # 40% - Most important
    EXPERIENCE = 0.25   # 25%
    EDUCATION = 0.15    # 15%
    PROJECTS = 0.20     # 20%


class EnhancedScorer:
    """
    Advanced scoring with multiple factors
    
    Old method (your current scorer.py):
    - Only keyword matching
    - Single score
    
    New method (this file):
    - Semantic understanding
    - 4 separate scores combined fairly
    - More accurate
    """
    
    def __init__(self):
        """Initialize with semantic matcher"""
        print("🔄 Initializing Enhanced Scorer...")
        self.matcher = SemanticMatcher()
        self.weights = ScoringWeights()
        print("✅ Enhanced Scorer ready!")
    
    def calculate_skill_score(
        self,
        resume_skills: List[str],
        job_skills: List[str],
        resume_text: str = "",
        job_text: str = ""
    ) -> Dict:
        """
        Score 1: Skills Match (40% of final score)
        
        Method:
        1. Count exact matches (40%)
        2. Semantic similarity (60%)
        
        Args:
            resume_skills: ['python', 'django', 'react']
            job_skills: ['python', 'flask', 'vue']
            resume_text: Full resume text
            job_text: Full job description
        
        Returns:
            {
                'score': 0.75,  # 75%
                'matched': ['python'],
                'missing': ['flask', 'vue']
            }
        """
        if not job_skills:
            return {'score': 0.0, 'matched': [], 'missing': []}
        
        # Convert to lowercase
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        # Exact matching
        matched = list(set(resume_skills_lower) & set(job_skills_lower))
        missing = list(set(job_skills_lower) - set(resume_skills_lower))
        
        exact_ratio = len(matched) / len(job_skills_lower)
        
        # Semantic matching
        if resume_text and job_text:
            semantic_score = self.matcher.semantic_similarity(
                resume_text,
                job_text
            )
        else:
            semantic_score = 0.0
        
        # Combine: 40% exact + 60% semantic
        final_score = (0.4 * exact_ratio) + (0.6 * semantic_score)
        
        return {
            'score': final_score,
            'exact_match': exact_ratio,
            'semantic_match': semantic_score,
            'matched_skills': matched,
            'missing_skills': missing,
            'match_count': f"{len(matched)}/{len(job_skills_lower)}"
        }
    
    def calculate_experience_score(
        self,
        candidate_years: float,
        required_years: float
    ) -> Dict:
        """
        Score 2: Experience (25% of final score)
        
        Method:
        - If candidate has >= required: 100%
        - If less: proportional score
        - Bonus for extra experience (up to 50% more)
        
        Args:
            candidate_years: 3.5
            required_years: 3
        
        Returns:
            {'score': 1.0, 'years_match': 'Exceeds'}
        """
        if required_years <= 0:
            return {'score': 1.0, 'status': 'Not specified'}
        
        ratio = candidate_years / required_years
        
        if ratio >= 1.5:
            score = 1.0
            status = "Far exceeds"
        elif ratio >= 1.0:
            score = 1.0
            status = "Meets/Exceeds"
        elif ratio >= 0.7:
            score = ratio
            status = "Close match"
        else:
            score = ratio * 0.8  # Penalty for low experience
            status = "Below requirement"
        
        return {
            'score': min(score, 1.0),
            'candidate_years': candidate_years,
            'required_years': required_years,
            'status': status
        }
    
    def calculate_education_score(
        self,
        candidate_degree: str,
        required_degree: str
    ) -> Dict:
        """
        Score 3: Education (15% of final score)
        
        Hierarchy: PhD > Master > Bachelor > Diploma
        
        Args:
            candidate_degree: 'bachelor'
            required_degree: 'bachelor'
        
        Returns:
            {'score': 1.0, 'level_match': 'Exact'}
        """
        degree_levels = {
            'phd': 4, 'doctorate': 4,
            'master': 3, 'masters': 3, 'msc': 3, 'mtech': 3, 'me': 3,
            'bachelor': 2, 'bachelors': 2, 'bsc': 2, 'btech': 2, 'be': 2,
            'diploma': 1,
            'none': 0, '': 0
        }
        
        cand_level = degree_levels.get(candidate_degree.lower().strip(), 0)
        req_level = degree_levels.get(required_degree.lower().strip(), 0)
        
        if req_level == 0:
            return {'score': 1.0, 'status': 'Not required'}
        
        if cand_level >= req_level:
            score = 1.0
            status = "Meets requirement"
        else:
            score = cand_level / req_level
            status = "Below requirement"
        
        return {
            'score': score,
            'candidate_level': candidate_degree,
            'required_level': required_degree,
            'status': status
        }
    
    def calculate_project_score(
        self,
        resume_projects: str,
        job_description: str
    ) -> Dict:
        """
        Score 4: Projects (20% of final score)
        
        Uses semantic similarity between projects and job
        
        Args:
            resume_projects: "Built AI chatbot, ML model"
            job_description: "Looking for ML engineer"
        
        Returns:
            {'score': 0.85}
        """
        if not resume_projects or not job_description:
            return {'score': 0.0, 'status': 'No projects found'}
        
        similarity = self.matcher.semantic_similarity(
            resume_projects,
            job_description
        )
        
        return {
            'score': similarity,
            'status': 'Relevant' if similarity > 0.6 else 'Some relevance'
        }
    
    def get_final_score(
        self,
        resume_data: Dict,
        job_data: Dict
    ) -> Dict:
        """
        Calculate complete score with all factors
        
        Args:
            resume_data: {
                'skills': ['python', 'django'],
                'years_experience': 3,
                'degree': 'bachelor',
                'full_text': '...',
                'projects_text': '...'
            }
            
            job_data: {
                'required_skills': ['python', 'flask'],
                'required_years': 3,
                'required_degree': 'bachelor',
                'full_text': '...'
            }
        
        Returns:
            {
                'final_score': 78.5,
                'breakdown': {...}
            }
        """
        print("\n🔍 Calculating multi-factor scores...\n")
        
        # Calculate each dimension
        skills = self.calculate_skill_score(
            resume_data.get('skills', []),
            job_data.get('required_skills', []),
            resume_data.get('full_text', ''),
            job_data.get('full_text', '')
        )
        
        experience = self.calculate_experience_score(
            resume_data.get('years_experience', 0),
            job_data.get('required_years', 0)
        )
        
        education = self.calculate_education_score(
            resume_data.get('degree', ''),
            job_data.get('required_degree', '')
        )
        
        projects = self.calculate_project_score(
            resume_data.get('projects_text', ''),
            job_data.get('full_text', '')
        )
        
        # Calculate weighted final score
        final_score = (
            self.weights.SKILLS * skills['score'] +
            self.weights.EXPERIENCE * experience['score'] +
            self.weights.EDUCATION * education['score'] +
            self.weights.PROJECTS * projects['score']
        ) * 100  # Convert to 0-100 scale
        
        return {
            'final_score': round(final_score, 2),
            'grade': self._get_grade(final_score),
            'breakdown': {
                'skills': {
                    'score': round(skills['score'] * 100, 1),
                    'weight': '40%',
                    'details': skills
                },
                'experience': {
                    'score': round(experience['score'] * 100, 1),
                    'weight': '25%',
                    'details': experience
                },
                'education': {
                    'score': round(education['score'] * 100, 1),
                    'weight': '15%',
                    'details': education
                },
                'projects': {
                    'score': round(projects['score'] * 100, 1),
                    'weight': '20%',
                    'details': projects
                }
            }
        }
    
    def _get_grade(self, score: float) -> str:
        """Convert score to grade"""
        if score >= 85:
            return "A - Excellent Match"
        elif score >= 70:
            return "B - Good Match"
        elif score >= 55:
            return "C - Average Match"
        elif score >= 40:
            return "D - Below Average"
        else:
            return "F - Poor Match"


# Test code
if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTING ENHANCED SCORER")
    print("="*60)
    
    # Initialize
    scorer = EnhancedScorer()
    
    # Sample data
    resume_data = {
        'skills': ['python', 'django', 'react', 'sql', 'git'],
        'years_experience': 3.5,
        'degree': 'bachelor',
        'full_text': 'Experienced Python developer with Django and React. Built multiple web applications.',
        'projects_text': 'E-commerce platform using Django. Real-time chat app with React.'
    }
    
    job_data = {
        'required_skills': ['python', 'django', 'postgresql', 'docker'],
        'required_years': 3,
        'required_degree': 'bachelor',
        'full_text': 'Looking for Python backend developer with Django experience and database skills.'
    }
    
    # Calculate scores
    result = scorer.get_final_score(resume_data, job_data)
    
    # Display results
    print(f"\n{'='*60}")
    print(f"FINAL SCORE: {result['final_score']}/100")
    print(f"GRADE: {result['grade']}")
    print(f"{'='*60}\n")
    
    print("BREAKDOWN:")
    for dimension, data in result['breakdown'].items():
        print(f"\n{dimension.upper()} ({data['weight']}):")
        print(f"  Score: {data['score']}/100")
        if 'matched_skills' in data['details']:
            print(f"  Matched: {data['details']['matched_skills']}")
            print(f"  Missing: {data['details']['missing_skills']}")
        if 'status' in data['details']:
            print(f"  Status: {data['details']['status']}")
    
    print(f"\n{'='*60}")
    print("✅ Test completed!")
    print(f"{'='*60}\n")