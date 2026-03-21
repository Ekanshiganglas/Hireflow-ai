"""
Data Visualizations for Resume Analytics
Creates charts and graphs for HR insights
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any
import pandas as pd


def create_score_distribution_chart(results: List[Dict]) -> go.Figure:
    """
    Create histogram of score distribution
    
    Args:
        results: List of candidate results
    
    Returns:
        Plotly figure
    """
    # Extract scores
    scores = []
    for r in results:
        if r['status'] == 'success':
            score = r.get('enhanced_score') or r.get('classic_score', 0)
            scores.append(score)
    
    if not scores:
        return None
    
    # Create histogram
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=scores,
        nbinsx=10,
        marker=dict(
            color=scores,
            colorscale='RdYlGn',
            line=dict(color='white', width=1)
        ),
        hovertemplate='Score Range: %{x}<br>Count: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Candidate Score Distribution',
        xaxis_title='Match Score (%)',
        yaxis_title='Number of Candidates',
        showlegend=False,
        height=400,
        hovermode='x unified'
    )
    
    # Add threshold lines
    fig.add_vline(x=70, line_dash="dash", line_color="green", 
                  annotation_text="Excellent (≥70%)")
    fig.add_vline(x=50, line_dash="dash", line_color="orange",
                  annotation_text="Good (≥50%)")
    
    return fig


def create_skills_chart(results: List[Dict], top_n: int = 10) -> go.Figure:
    """
    Create bar chart of most common skills
    
    Args:
        results: List of candidate results
        top_n: Number of top skills to show
    
    Returns:
        Plotly figure
    """
    # Count all skills
    skill_counts = {}
    for r in results:
        if r['status'] == 'success':
            for skill in r.get('skills', []):
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
    
    if not skill_counts:
        return None
    
    # Sort and get top N
    sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    skills = [s[0] for s in sorted_skills]
    counts = [s[1] for s in sorted_skills]
    
    # Create bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=skills,
        x=counts,
        orientation='h',
        marker=dict(
            color=counts,
            colorscale='Blues',
            line=dict(color='darkblue', width=1)
        ),
        hovertemplate='<b>%{y}</b><br>Found in %{x} candidates<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'Top {top_n} Most Common Skills',
        xaxis_title='Number of Candidates',
        yaxis_title='Skill',
        height=400,
        showlegend=False
    )
    
    return fig


def create_skill_gap_chart(skill_gaps: Dict) -> go.Figure:
    """
    Create chart showing most common missing skills
    
    Args:
        skill_gaps: Skill gap analysis data
    
    Returns:
        Plotly figure
    """
    if not skill_gaps or not skill_gaps.get('most_common_gaps'):
        return None
    
    gaps = skill_gaps['most_common_gaps'][:10]  # Top 10
    
    skills = [g['skill'] for g in gaps]
    percentages = [g['percentage'] for g in gaps]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=skills,
        x=percentages,
        orientation='h',
        marker=dict(
            color='rgba(255, 99, 71, 0.6)',
            line=dict(color='rgba(255, 99, 71, 1)', width=2)
        ),
        hovertemplate='<b>%{y}</b><br>Missing in %{x:.1f}% of candidates<extra></extra>'
    ))
    
    fig.update_layout(
        title='Most Common Skill Gaps',
        xaxis_title='Percentage of Candidates Missing This Skill (%)',
        yaxis_title='Skill',
        height=400,
        showlegend=False
    )
    
    return fig


def create_grade_distribution_pie(results: List[Dict]) -> go.Figure:
    """
    Create pie chart of grade distribution
    
    Args:
        results: List of candidate results
    
    Returns:
        Plotly figure
    """
    # Count grades
    grade_counts = {}
    for r in results:
        if r['status'] == 'success' and r.get('grade'):
            # Extract letter grade (A, B, C, D, F)
            grade_letter = r['grade'].split(' -')[0].strip()
            grade_counts[grade_letter] = grade_counts.get(grade_letter, 0) + 1
    
    if not grade_counts:
        return None
    
    labels = list(grade_counts.keys())
    values = list(grade_counts.values())
    
    colors = {
        'A': '#28a745',  # Green
        'B': '#ffc107',  # Yellow
        'C': '#fd7e14',  # Orange
        'D': '#dc3545',  # Red
        'F': '#6c757d'   # Gray
    }
    
    color_list = [colors.get(label, '#6c757d') for label in labels]
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=color_list),
        hovertemplate='<b>Grade %{label}</b><br>%{value} candidates (%{percent})<extra></extra>'
    ))
    
    fig.update_layout(
        title='Candidate Grade Distribution',
        height=400
    )
    
    return fig


def create_comparison_radar(candidates: List[Dict], score_type: str = 'enhanced') -> go.Figure:
    """
    Create radar chart comparing top candidates
    
    Args:
        candidates: List of candidate data (max 5)
        score_type: 'enhanced' or 'classic'
    
    Returns:
        Plotly figure
    """
    if not candidates or len(candidates) == 0:
        return None
    
    # Limit to top 5
    candidates = candidates[:5]
    
    fig = go.Figure()
    
    for candidate in candidates:
        if score_type == 'enhanced' and candidate.get('breakdown'):
            breakdown = candidate['breakdown']
            
            categories = ['Skills', 'Experience', 'Education', 'Projects']
            values = [
                breakdown['skills']['score'],
                breakdown['experience']['score'],
                breakdown['education']['score'],
                breakdown['projects']['score']
            ]
            
            # Close the radar chart
            values.append(values[0])
            categories_closed = categories + [categories[0]]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories_closed,
                fill='toself',
                name=candidate['name'][:20],  # Truncate long names
                hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}%<extra></extra>'
            ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title='Top Candidates Comparison (Multi-Factor Breakdown)',
        height=500,
        showlegend=True
    )
    
    return fig


# Test code
if __name__ == "__main__":
    print("📊 Visualization Module")
    print("Use with batch_processor results for charts")