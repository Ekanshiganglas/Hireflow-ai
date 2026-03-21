# app_final.py
# HireFlow AI - Optimized Fast Loading Version
# AI-Powered Resume Analysis & Candidate Matching Platform

import streamlit as st
import pandas as pd
import tempfile
import os
from datetime import datetime
import time

# Page config - MUST be first
st.set_page_config(
    page_title="HireFlow AI - Resume Analysis Platform",
    page_icon="🎯",
    layout="wide"
)

# Loading optimization - lazy load heavy modules
@st.cache_resource
def load_batch_processor():
    """Load batch processor with caching"""
    try:
        from batch_processor import BatchProcessor
        return BatchProcessor, True
    except Exception as e:
        st.error(f"Batch processor not available: {e}")
        return None, False

@st.cache_resource
def load_visualizations():
    """Load visualization functions with caching"""
    try:
        from visualizations import (
            create_score_distribution_chart,
            create_skills_chart,
            create_skill_gap_chart,
            create_grade_distribution_pie,
            create_comparison_radar
        )
        return {
            'score_dist': create_score_distribution_chart,
            'skills': create_skills_chart,
            'skill_gap': create_skill_gap_chart,
            'grade_pie': create_grade_distribution_pie,
            'radar': create_comparison_radar
        }
    except Exception as e:
        st.warning(f"Visualizations not available: {e}")
        return None

@st.cache_resource
def load_enhanced_scorer():
    """Load enhanced scorer with caching"""
    try:
        from scoring_engine import EnhancedScorer
        return EnhancedScorer, True
    except Exception as e:
        return None, False

# Import basic modules (fast)
from parser import extract_text
from extractor import extract_all
from scorer import calculate_match_score, get_matching_keywords
from suggester import get_resume_suggestions

# Custom CSS
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'mode' not in st.session_state:
    st.session_state.mode = 'single'
if 'batch_results' not in st.session_state:
    st.session_state.batch_results = None
if 'processor' not in st.session_state:
    st.session_state.processor = None

# Header
st.title("🎯 HireFlow AI")
st.markdown("**AI-Powered Resume Analysis & Candidate Matching Platform**")

# Mode selector
st.markdown("---")
mode_col1, mode_col2, mode_col3 = st.columns([2, 1, 2])

with mode_col2:
    mode = st.radio(
        "Choose Mode:",
        ["🎯 Single Resume", "📊 Batch Processing"],
        horizontal=True,
        key="mode_selector"
    )

st.session_state.mode = 'single' if 'Single' in mode else 'batch'

# Show mode description
if st.session_state.mode == 'single':
    st.info("📄 **Single Resume Mode** - Upload one resume, get detailed analysis with AI suggestions")
else:
    st.info("📊 **Batch Processing Mode** - Upload multiple resumes, compare candidates, analyze trends")

st.markdown("---")

# ========================================
# SINGLE RESUME MODE
# ========================================
if st.session_state.mode == 'single':
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📄 Step 1: Upload Resume")
        uploaded_file = st.file_uploader(
            "Choose a PDF or DOCX file",
            type=["pdf", "docx"],
            help="Upload the candidate's resume",
            key="single_upload"
        )
        
        if uploaded_file:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    with col2:
        st.header("💼 Step 2: Job Description")
        job_description = st.text_area(
            "Paste the job posting here",
            height=200,
            placeholder="Senior Software Developer\n\nRequired Skills:\n- Python\n- Django\n...",
            key="single_job_desc"
        )
        
        if job_description.strip():
            st.info(f"📝 {len(job_description.split())} words")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button(
            "🔍 Analyze Resume",
            type="primary",
            use_container_width=True,
            disabled=not (uploaded_file and job_description.strip())
        )
    
    if analyze_button:
        with st.spinner("🔄 Analyzing resume..."):
            try:
                # Save temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
                
                # Extract and analyze
                resume_text = extract_text(tmp_path)
                info = extract_all(resume_text)
                score = calculate_match_score(resume_text, job_description)
                keywords = get_matching_keywords(resume_text, job_description)
                
                # Try enhanced scoring
                enhanced_result = None
                EnhancedScorer, ENHANCED_AVAILABLE = load_enhanced_scorer()
                
                if ENHANCED_AVAILABLE:
                    with st.spinner("🤖 Calculating AI scores..."):
                        scorer = EnhancedScorer()
                        
                        resume_data = {
                            'skills': info['skills'],
                            'years_experience': 3,
                            'degree': 'bachelor',
                            'full_text': resume_text,
                            'projects_text': resume_text
                        }
                        
                        job_data = {
                            'required_skills': keywords['matched'] + keywords['missing'],
                            'required_years': 3,
                            'required_degree': 'bachelor',
                            'full_text': job_description
                        }
                        
                        enhanced_result = scorer.get_final_score(resume_data, job_data)
                
                os.unlink(tmp_path)
                
                # Display results
                st.markdown("---")
                st.header("📊 Analysis Results")
                
                st.subheader("🎯 Match Scoring")
                
                if enhanced_result:
                    score_col1, score_col2 = st.columns(2)
                    
                    with score_col1:
                        st.markdown("### 📈 Classic Score")
                        if score >= 70:
                            st.success(f"# {score}%")
                        elif score >= 50:
                            st.warning(f"# {score}%")
                        else:
                            st.error(f"# {score}%")
                        st.progress(score / 100)
                    
                    with score_col2:
                        st.markdown("### 🤖 Enhanced AI Score")
                        enhanced_score = enhanced_result['final_score']
                        if enhanced_score >= 70:
                            st.success(f"# {enhanced_score}%")
                        elif enhanced_score >= 50:
                            st.warning(f"# {enhanced_score}%")
                        else:
                            st.error(f"# {enhanced_score}%")
                        st.progress(enhanced_score / 100)
                        st.info(enhanced_result['grade'])
                    
                    st.markdown("### 📊 Score Breakdown")
                    breakdown = enhanced_result['breakdown']
                    
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    
                    with metric_col1:
                        st.metric("💼 Skills", f"{breakdown['skills']['score']}%", 
                                 delta=f"Weight: {breakdown['skills']['weight']}")
                    with metric_col2:
                        st.metric("⏱️ Experience", f"{breakdown['experience']['score']}%",
                                 delta=f"Weight: {breakdown['experience']['weight']}")
                    with metric_col3:
                        st.metric("🎓 Education", f"{breakdown['education']['score']}%",
                                 delta=f"Weight: {breakdown['education']['weight']}")
                    with metric_col4:
                        st.metric("🚀 Projects", f"{breakdown['projects']['score']}%",
                                 delta=f"Weight: {breakdown['projects']['weight']}")
                else:
                    if score >= 70:
                        st.success(f"# {score}%")
                        st.success("✅ EXCELLENT MATCH!")
                    elif score >= 50:
                        st.warning(f"# {score}%")
                        st.warning("⚠️ GOOD MATCH")
                    else:
                        st.error(f"# {score}%")
                        st.error("❌ WEAK MATCH")
                    st.progress(score / 100)
                
                st.markdown("---")
                
                st.subheader("🎯 Skills Analysis")
                skill_col1, skill_col2 = st.columns(2)
                
                with skill_col1:
                    st.markdown("### ✅ Matching Skills")
                    if keywords['matched']:
                        for skill in keywords['matched']:
                            st.markdown(f"- ✅ {skill}")
                    else:
                        st.info("No exact matches")
                    
                    st.metric("Match Count", 
                             f"{keywords['match_count']}/{keywords['total_required']}",
                             f"{round(keywords['match_count']/keywords['total_required']*100) if keywords['total_required'] > 0 else 0}%")
                
                with skill_col2:
                    st.markdown("### ❌ Missing Skills")
                    if keywords['missing']:
                        for skill in keywords['missing']:
                            st.markdown(f"- ❌ {skill}")
                    else:
                        st.success("No missing skills!")
                
                st.markdown("---")
                
                st.subheader("👤 Candidate Information")
                info_col1, info_col2, info_col3 = st.columns(3)
                
                with info_col1:
                    st.metric("Name", info['name'])
                with info_col2:
                    st.metric("Email", info['email'])
                with info_col3:
                    st.metric("Phone", info['phone'])
                
                with st.expander("📋 All Detected Skills"):
                    if info['skills']:
                        st.write(", ".join(info['skills']))
                        st.info(f"Total: {len(info['skills'])} skills")
                    else:
                        st.warning("No skills detected")
                
                st.markdown("---")
                
                st.header("🤖 AI-Powered Improvement Suggestions")
                
                with st.spinner("Generating suggestions..."):
                    suggestions = get_resume_suggestions(
                        resume_text,
                        job_description,
                        score,
                        keywords['matched'],
                        keywords['missing']
                    )
                
                with st.expander("📋 View Detailed Suggestions", expanded=True):
                    st.text(suggestions)
                
                st.markdown("---")
                st.success("✅ Analysis complete!")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ========================================
# BATCH PROCESSING MODE
# ========================================
else:
    
    # Load batch processor
    BatchProcessor, BATCH_AVAILABLE = load_batch_processor()
    
    if not BATCH_AVAILABLE:
        st.error("❌ Batch processing not available. Please check installation.")
        st.stop()
    
    # Tabs for batch mode
    tab1, tab2, tab3 = st.tabs([
        "📤 Upload & Process",
        "🏆 Rankings",
        "📊 Analytics"
    ])
    
    with tab1:
        st.header("📤 Batch Resume Upload")
        
        job_description = st.text_area(
            "📋 Job Description",
            height=200,
            placeholder="Senior Software Developer\n\nRequired Skills:\n- Python\n- Django\n...",
            key="batch_job_desc"
        )
        
        st.markdown("---")
        
        st.subheader("📁 Upload Multiple Resumes")
        uploaded_files = st.file_uploader(
            "Select multiple resume files",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            key="batch_upload"
        )
        
        if uploaded_files:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Files", len(uploaded_files))
            with col2:
                total_size = sum(f.size for f in uploaded_files) / (1024 * 1024)
                st.metric("Size", f"{total_size:.2f} MB")
            with col3:
                pdf_count = sum(1 for f in uploaded_files if f.name.endswith('.pdf'))
                st.metric("PDF/DOCX", f"{pdf_count}/{len(uploaded_files)-pdf_count}")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            process_button = st.button(
                f"🚀 Analyze {len(uploaded_files) if uploaded_files else 0} Resume(s)",
                type="primary",
                use_container_width=True,
                disabled=not (uploaded_files and job_description.strip())
            )
        
        if process_button:
            with st.spinner("Processing..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(progress, message):
                    progress_bar.progress(progress)
                    status_text.text(message)
                
                processor = BatchProcessor(job_description)
                results = processor.process_batch(uploaded_files, progress_callback=update_progress)
                
                st.session_state.batch_results = results
                st.session_state.processor = processor
                
                progress_bar.empty()
                status_text.empty()
                
                stats = processor.get_statistics()
                
                st.balloons()
                st.success(f"✅ Processed {stats['successful']} resumes!")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total", stats['total_processed'])
                with col2:
                    st.metric("Avg Score", f"{stats['average_score']:.1f}%")
                with col3:
                    st.metric("Highest", f"{stats['highest_score']:.1f}%")
                with col4:
                    st.metric("Top (≥70%)", stats['candidates_above_70'])
    
    with tab2:
        st.header("🏆 Candidate Rankings")
        
        if st.session_state.batch_results is None:
            st.info("Upload resumes in the first tab")
        else:
            processor = st.session_state.processor
            
            filter_col1, filter_col2 = st.columns(2)
            
            with filter_col1:
                min_score = st.slider("Minimum Score", 0, 100, 0, 5)
            
            with filter_col2:
                search = st.text_input("🔎 Search", placeholder="Name, email, skill...")
            
            ranked = processor.get_ranked_results('classic')
            
            # Apply filters
            filtered = ranked
            if min_score > 0:
                filtered = [r for r in filtered if r['classic_score'] >= min_score]
            
            if search:
                search_lower = search.lower()
                filtered = [r for r in filtered 
                           if search_lower in r['name'].lower() 
                           or search_lower in r['email'].lower()
                           or any(search_lower in s.lower() for s in r['skills'])]
            
            for idx, r in enumerate(filtered):
                r['rank'] = idx + 1
            
            st.markdown(f"### Showing {len(filtered)} of {len(ranked)} candidates")
            
            if filtered:
                display_data = []
                for r in filtered:
                    score = r['classic_score']
                    emoji = "🟢" if score >= 70 else "🟡" if score >= 50 else "🔴"
                    
                    display_data.append({
                        '': emoji,
                        'Rank': r['rank'],
                        'Name': r['name'],
                        'Email': r['email'],
                        'Score': f"{score:.1f}%",
                        'Skills': r['skill_count'],
                        'Matched': f"{r['match_count']}/{r['total_required']}",
                        'File': r['filename']
                    })
                
                df = pd.DataFrame(display_data)
                st.dataframe(df, use_container_width=True, height=400)
                
                st.markdown("---")
                csv = df.to_csv(index=False)
                st.download_button(
                    "📄 Download CSV",
                    csv,
                    f"rankings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    "text/csv"
                )
    
    with tab3:
        st.header("📊 Analytics Dashboard")
        
        if st.session_state.batch_results is None:
            st.info("Upload resumes first")
        else:
            processor = st.session_state.processor
            stats = processor.get_statistics()
            skill_gaps = processor.get_skill_gap_analysis()
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total", stats['total_processed'])
            with col2:
                st.metric("Avg", f"{stats['average_score']:.1f}%")
            with col3:
                st.metric("≥70%", stats['candidates_above_70'])
            with col4:
                st.metric("50-70%", stats['candidates_50_to_70'])
            with col5:
                st.metric("<50%", stats['candidates_below_50'])
            
            st.markdown("---")
            
            # Load and show visualizations
            viz_funcs = load_visualizations()
            
            if viz_funcs:
                viz_col1, viz_col2 = st.columns(2)
                
                with viz_col1:
                    chart = viz_funcs['score_dist'](st.session_state.batch_results)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                
                with viz_col2:
                    chart = viz_funcs['grade_pie'](st.session_state.batch_results)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                
                st.markdown("---")
                
                viz_col3, viz_col4 = st.columns(2)
                
                with viz_col3:
                    chart = viz_funcs['skills'](st.session_state.batch_results)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                
                with viz_col4:
                    chart = viz_funcs['skill_gap'](skill_gaps)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
            else:
                st.warning("Visualizations not available")

# Sidebar
with st.sidebar:
    st.header("ℹ️ HireFlow AI")
    
    st.markdown("---")
    
    st.markdown("""
    ### 🚀 Features
    
    **Single Mode:**
    - ✅ Detailed analysis
    - ✅ AI suggestions
    - ✅ Score breakdown
    
    **Batch Mode:**
    - ✅ Multi-resume upload
    - ✅ Candidate ranking
    - ✅ Analytics dashboard
    - ✅ Export reports
    
    ### 💡 Quick Tip
    Use **Single Mode** for detailed review.
    Use **Batch Mode** for screening many applicants.
    """)
    
    st.markdown("---")
    
    if st.session_state.mode == 'batch' and st.session_state.batch_results:
        st.success(f"✅ {len(st.session_state.batch_results)} resumes loaded")
        
        if st.button("🗑️ Clear Data"):
            st.session_state.batch_results = None
            st.session_state.processor = None
            st.rerun()
    
    st.markdown("---")
    st.markdown("**HireFlow AI v1.0**")
    st.markdown("*Fast Loading Edition*")