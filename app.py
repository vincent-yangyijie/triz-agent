import streamlit as st
import os
from llm_engine import LLMEngine
from skills_lib import SKILLS, get_skill_by_id

# Page Config
st.set_page_config(
    page_title="TRIZ Automation Agent",
    page_icon="🔧",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 4px;
    }
    .skill-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🔧 TRIZ Automation Agent (Skills 1-10)")
st.markdown("**Automated Engineering Problem Solving using TRIZ Methodology**")
st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    model_provider = st.selectbox(
        "Select LLM Provider",
        ["DeepSeek", "Kimi"],
        index=0
    )
    
    st.info(f"Using **{model_provider}** API")
    
    # Initialize LLM Engine
    try:
        if "llm" not in st.session_state or st.session_state.current_provider != model_provider:
            st.session_state.llm = LLMEngine(provider=model_provider)
            st.session_state.current_provider = model_provider
        st.success("✅ LLM Connected!")
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        st.stop()
    
    st.markdown("---")
    st.header("📋 Skills Overview")
    for skill in SKILLS:
        st.markdown(f"**{skill.id}.** {skill.name.split('(')[0].strip()}")

# Main Input Section
st.subheader("📥 1. Problem Input")

# File Upload
uploaded_file = st.file_uploader(
    "Upload Patent/Document (PDF, DOCX, TXT, MD)", 
    type=["pdf", "docx", "txt", "md"]
)

def read_pdf(file):
    import pypdf
    reader = pypdf.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def read_docx(file):
    import docx
    doc = docx.Document(file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

file_content = ""
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".pdf"):
            file_content = read_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            file_content = read_docx(uploaded_file)
        elif uploaded_file.name.endswith(".txt") or uploaded_file.name.endswith(".md"):
            file_content = uploaded_file.read().decode("utf-8")
        st.success(f"✅ File '{uploaded_file.name}' loaded successfully! ({len(file_content)} characters)")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

# Text Area
if file_content:
    default_text = file_content
else:
    default_text = ""

user_input = st.text_area(
    "Describe the Patent or Engineering Problem:",
    value=default_text,
    height=200,
    placeholder="Paste patent text or describe the technical problem here..."
)

# Session State for Results
if "results" not in st.session_state:
    st.session_state.results = {}

st.markdown("---")

# Analysis Options
st.subheader("🚀 2. Analysis Options")

col1, col2, col3 = st.columns(3)

with col1:
    run_skill1 = st.button("▶️ Run Skill 1 Only", use_container_width=True)

with col2:
    run_all = st.button("⚡ Run All Skills (1-10)", use_container_width=True)

with col3:
    clear_results = st.button("🗑️ Clear Results", use_container_width=True)

if clear_results:
    st.session_state.results = {}
    st.rerun()

# Run Skill 1 Only
if run_skill1:
    if not user_input:
        st.warning("⚠️ Please provide input text.")
    else:
        with st.spinner("🔄 Analyzing Skill 1: Engineering Clarification..."):
            skill = get_skill_by_id(1)
            prompt = skill.render_prompt(user_input)
            response = st.session_state.llm.generate(prompt)
            st.session_state.results[1] = response
        st.success("✅ Skill 1 Complete!")
        st.rerun()

# Run All Skills
if run_all:
    if not user_input:
        st.warning("⚠️ Please provide input text.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for skill in SKILLS:
            status_text.text(f"🔄 Processing {skill.name}...")
            prompt = skill.render_prompt(user_input)
            
            with st.spinner(f"Generating {skill.name}..."):
                response = st.session_state.llm.generate(prompt)
                st.session_state.results[skill.id] = response
            
            progress_bar.progress(skill.id / 10)
        
        status_text.text("✅ All Skills Complete!")
        st.success("🎉 Full Analysis Complete!")
        st.rerun()

# Display Results
if len(st.session_state.results) > 0:
    st.markdown("---")
    st.subheader("📊 3. Analysis Results")
    
    # Create tabs for each skill
    tab_names = [f"Skill {s.id}" for s in SKILLS]
    tabs = st.tabs(tab_names)
    
    for i, skill in enumerate(SKILLS):
        with tabs[i]:
            st.markdown(f"### {skill.name}")
            st.caption(skill.description)
            
            if skill.id in st.session_state.results:
                st.markdown(st.session_state.results[skill.id])
                
                # Download Button
                st.download_button(
                    label=f"📥 Download Skill {skill.id} Result",
                    data=st.session_state.results[skill.id],
                    file_name=f"skill_{skill.id}_output.md",
                    mime="text/markdown",
                    key=f"download_{skill.id}"
                )
            else:
                st.info("🔘 Run the analysis to see results.")

# Export All - Sidebar
if len(st.session_state.results) > 0:
    st.sidebar.markdown("---")
    st.sidebar.header("📥 Export")
    
    # Generate Full Report
    full_report = f"# TRIZ Analysis Report\n\n"
    full_report += f"## Original Input\n\n{user_input[:500]}...\n\n---\n\n"
    
    for skill in SKILLS:
        if skill.id in st.session_state.results:
            full_report += f"## {skill.name}\n\n{st.session_state.results[skill.id]}\n\n---\n\n"
    
    st.sidebar.download_button(
        label="📥 Download Full Report",
        data=full_report,
        file_name="TRIZ_Full_Report.md",
        mime="text/markdown"
    )
    
    # Show completion status
    completed = len(st.session_state.results)
    st.sidebar.metric("Skills Completed", f"{completed}/10")

# Footer
st.markdown("---")
st.caption("TRIZ Automation Agent v2.0 | Powered by DeepSeek/Kimi API")
