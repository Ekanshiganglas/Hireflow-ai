"""
Batch Resume Processor
Handles multiple resume uploads and processing
"""

import os
import tempfile
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd

# Import existing modules
from parser import extract_text
from extractor import extract_all
from scorer import calculate_match_score, get_matching_keywords

# Import Phase 1 modules
try:
    from scoring_engine import EnhancedScorer
    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False


class BatchProcessor:
    """
    Process multiple resumes against a job description
    
    Workflow:
    1. Upload multiple files
    2. Extract text from each
    3. Score each against job description
    4. Rank all candidates
    5. Generate analytics
    """
    
    def __init__(self, job_description: str):
        """
        Initialize batch processor
        
        Args:
            job_description: The job posting to match against
        """
        self.job_description = job_description
        self.results = []
        self.processed_count = 0
        self.failed_count = 0
        
        # Initialize enhanced scorer if available
        if ENHANCED_AVAILABLE:
            print("🤖 Initializing Enhanced AI Scorer...")
            self.enhanced_scorer = EnhancedScorer()
        else:
            self.enhanced_scorer = None
            print("⚠️ Enhanced scoring not available")
    
    def process_single_resume(
        self, 
        file_path: str, 
        filename: str
    ) -> Dict[str, Any]:
        """
        Process a single resume file
        
        Args:
            file_path: Path to resume file
            filename: Original filename
        
        Returns:
            Dictionary with all analysis results
        """
        try:
            # Extract text
            resume_text = extract_text(file_path)
            
            if not resume_text or len(resume_text.strip()) < 50:
                raise ValueError("Resume text too short or empty")
            
            # Extract information
            info = extract_all(resume_text)
            
            # Calculate classic score
            classic_score = calculate_match_score(resume_text, self.job_description)
            keywords = get_matching_keywords(resume_text, self.job_description)
            
            # Calculate enhanced score if available
            enhanced_result = None
            if self.enhanced_scorer:
                resume_data = {
                    'skills': info['skills'],
                    'years_experience': 3,  # Default
                    'degree': 'bachelor',
                    'full_text': resume_text,
                    'projects_text': resume_text
                }
                
                job_data = {
                    'required_skills': keywords['matched'] + keywords['missing'],
                    'required_years': 3,
                    'required_degree': 'bachelor',
                    'full_text': self.job_description
                }
                
                enhanced_result = self.enhanced_scorer.get_final_score(resume_data, job_data)
            
            # Compile result
            result = {
                'filename': filename,
                'name': info['name'],
                'email': info['email'],
                'phone': info['phone'],
                'skills': info['skills'],
                'skill_count': len(info['skills']),
                'classic_score': classic_score,
                'enhanced_score': enhanced_result['final_score'] if enhanced_result else None,
                'grade': enhanced_result['grade'] if enhanced_result else None,
                'matched_skills': keywords['matched'],
                'missing_skills': keywords['missing'],
                'match_count': keywords['match_count'],
                'total_required': keywords['total_required'],
                'skill_match_ratio': keywords['match_count'] / keywords['total_required'] if keywords['total_required'] > 0 else 0,
                'breakdown': enhanced_result['breakdown'] if enhanced_result else None,
                'resume_text': resume_text,
                'processed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'success'
            }
            
            self.processed_count += 1
            return result
            
        except Exception as e:
            self.failed_count += 1
            return {
                'filename': filename,
                'name': 'ERROR',
                'email': 'N/A',
                'phone': 'N/A',
                'skills': [],
                'skill_count': 0,
                'classic_score': 0,
                'enhanced_score': 0,
                'grade': 'F - Error',
                'matched_skills': [],
                'missing_skills': [],
                'match_count': 0,
                'total_required': 0,
                'skill_match_ratio': 0,
                'breakdown': None,
                'resume_text': '',
                'processed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'failed',
                'error': str(e)
            }
    
    def process_batch(
        self, 
        uploaded_files: List[Any], 
        progress_callback=None
    ) -> List[Dict[str, Any]]:
        """
        Process multiple resume files
        
        Args:
            uploaded_files: List of uploaded file objects
            progress_callback: Optional callback function for progress updates
        
        Returns:
            List of result dictionaries
        """
        self.results = []
        total_files = len(uploaded_files)
        
        print(f"\n📦 Processing {total_files} resumes...")
        
        for idx, uploaded_file in enumerate(uploaded_files):
            # Update progress
            if progress_callback:
                progress = (idx + 1) / total_files
                progress_callback(progress, f"Processing {uploaded_file.name}...")
            
            print(f"  [{idx+1}/{total_files}] Processing: {uploaded_file.name}")
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=os.path.splitext(uploaded_file.name)[1]
            ) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            
            # Process resume
            result = self.process_single_resume(tmp_path, uploaded_file.name)
            self.results.append(result)
            
            # Clean up
            os.unlink(tmp_path)
        
        print(f"\n✅ Batch processing complete!")
        print(f"   Successful: {self.processed_count}")
        print(f"   Failed: {self.failed_count}")
        
        return self.results
    
    def get_ranked_results(self, score_type: str = 'enhanced') -> List[Dict[str, Any]]:
        """
        Get results ranked by score
        
        Args:
            score_type: 'enhanced' or 'classic'
        
        Returns:
            Sorted list of results (highest score first)
        """
        if not self.results:
            return []
        
        score_key = 'enhanced_score' if score_type == 'enhanced' and ENHANCED_AVAILABLE else 'classic_score'
        
        # Filter out failed results and sort
        successful_results = [r for r in self.results if r['status'] == 'success']
        ranked = sorted(successful_results, key=lambda x: x[score_key], reverse=True)
        
        # Add rank
        for idx, result in enumerate(ranked):
            result['rank'] = idx + 1
        
        return ranked
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Generate summary statistics
        
        Returns:
            Dictionary with statistics
        """
        if not self.results:
            return {}
        
        successful_results = [r for r in self.results if r['status'] == 'success']
        
        if not successful_results:
            return {
                'total_processed': len(self.results),
                'successful': 0,
                'failed': self.failed_count
            }
        
        scores = [r['enhanced_score'] if r['enhanced_score'] else r['classic_score'] 
                  for r in successful_results]
        
        return {
            'total_processed': len(self.results),
            'successful': self.processed_count,
            'failed': self.failed_count,
            'average_score': sum(scores) / len(scores) if scores else 0,
            'highest_score': max(scores) if scores else 0,
            'lowest_score': min(scores) if scores else 0,
            'candidates_above_70': sum(1 for s in scores if s >= 70),
            'candidates_50_to_70': sum(1 for s in scores if 50 <= s < 70),
            'candidates_below_50': sum(1 for s in scores if s < 50),
        }
    
    def get_skill_gap_analysis(self) -> Dict[str, Any]:
        """
        Analyze skill gaps across all candidates
        
        Returns:
            Dictionary with skill gap insights
        """
        if not self.results:
            return {}
        
        successful_results = [r for r in self.results if r['status'] == 'success']
        
        # Count missing skills
        skill_gaps = {}
        for result in successful_results:
            for skill in result['missing_skills']:
                skill_gaps[skill] = skill_gaps.get(skill, 0) + 1
        
        # Sort by frequency
        sorted_gaps = sorted(skill_gaps.items(), key=lambda x: x[1], reverse=True)
        
        total_candidates = len(successful_results)
        
        return {
            'total_candidates': total_candidates,
            'unique_missing_skills': len(skill_gaps),
            'most_common_gaps': [
                {
                    'skill': skill,
                    'missing_count': count,
                    'percentage': (count / total_candidates * 100) if total_candidates > 0 else 0
                }
                for skill, count in sorted_gaps[:10]  # Top 10
            ]
        }
    
    def export_to_dataframe(self) -> pd.DataFrame:
        """
        Export results to pandas DataFrame
        
        Returns:
            DataFrame with all results
        """
        if not self.results:
            return pd.DataFrame()
        
        # Select key fields for export
        export_data = []
        for result in self.results:
            export_data.append({
                'Rank': result.get('rank', '-'),
                'Name': result['name'],
                'Email': result['email'],
                'Phone': result['phone'],
                'Enhanced Score': result['enhanced_score'] if result['enhanced_score'] else '-',
                'Classic Score': result['classic_score'],
                'Grade': result['grade'] if result.get('grade') else '-',
                'Skills Count': result['skill_count'],
                'Matched Skills': ', '.join(result['matched_skills'][:5]),  # First 5
                'Missing Skills': ', '.join(result['missing_skills'][:5]),   # First 5
                'Status': result['status'],
                'Filename': result['filename']
            })
        
        return pd.DataFrame(export_data)


# Test code
if __name__ == "__main__":
    print("\n" + "="*60)
    print("BATCH PROCESSOR TEST")
    print("="*60 + "\n")
    
    print("ℹ️  This is a test module.")
    print("   Use with Streamlit app for full functionality.")
    print("\n" + "="*60)