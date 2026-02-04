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

# Title
st.title("🔧 TRIZ Automation Agent (Skills 1-14)")
st.markdown("Automated Engineering Problem Solving using TRIZ Methodology.")

# Sidebar - Configuration
with st.sidebar:
    st.header("Configuration")
    model_provider = st.selectbox(
        "Select LLM Provider",
        ["DeepSeek", "Kimi"],
        index=0
    )
    
    st.info(f"Using **{model_provider}** API via OpenAI Client.")
    
    # Initialize LLM Engine
    try:
        if "llm" not in st.session_state or st.session_state.current_provider != model_provider:
            st.session_state.llm = LLMEngine(provider=model_provider)
            st.session_state.current_provider = model_provider
        st.success("LLM Connected!")
    except Exception as e:
        st.error(f"Connection Error: {e}")
        st.stop()

# Main Input
st.subheader("1. Problem Input")

# File Upload
uploaded_file = st.file_uploader("Upload Patent/Document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

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
        elif uploaded_file.name.endswith(".txt"):
            file_content = uploaded_file.read().decode("utf-8")
        st.success(f"File '{uploaded_file.name}' loaded successfully!")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Text Area (Manual Input or File Content)
# If a file is uploaded, we pre-fill the text area (optional) or just use the variable.
# User flow: User can upload OR type. If upload, it populates the area for editing.
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

# Step 1: Clarification
if st.button("🚀 Analyze Step 1: Engineering Clarification"):
    if not user_input:
        st.warning("Please provide input text.")
    else:
        with st.spinner("Analyzing Skill 1: Engineering Clarification..."):
            skill = get_skill_by_id(1)
            prompt = skill.render_prompt(user_input)
            response = st.session_state.llm.generate(prompt)
            st.session_state.results[1] = response
            st.success("Skill 1 Complete!")

# Display Step 1 Result
if 1 in st.session_state.results:
    with st.expander("Skill 1: Engineering Clarification Result", expanded=True):
        st.markdown(st.session_state.results[1])

    # Context for next steps
    # We use the Clarified Output + Original Input as context for deep analysis, 
    # or just Original Input. Let's use Original Input to ensure full context, 
    # but append the Clarification summary if needed. 
    # For now, we stick to passing the Original Input to strictly follow "Skill X template".
    context_text = user_input

    # Step 2-14 Pipeline
    st.subheader("2. Full TRIZ Analysis (Skills 2-14)")
    if st.button("⚡ Run Skills 2-14 Sequence"):
        progress_bar = st.progress(0)
        
        for skill in SKILLS:
            if skill.id == 1:
                continue # Already done
                
            st.write(f"Processing **{skill.name}**...")
        
            # Construct Prompt
            # Some skills might benefit from previous outputs, but the templates take {{input}}.
            # We pass the User Input.
            prompt = skill.render_prompt(context_text)
            
            with st.spinner(f"Generating {skill.name}..."):
                response = st.session_state.llm.generate(prompt)
                st.session_state.results[skill.id] = response
            
            # Update Progress
            progress_bar.progress(skill.id / 14)
        
        st.success("Full Analysis Complete!")

# Display All Results
if len(st.session_state.results) > 1:
    st.subheader("Analysis Results")
    tabs = st.tabs([s.name for s in SKILLS])
    
    for i, skill in enumerate(SKILLS):
        with tabs[i]:
            if skill.id in st.session_state.results:
                st.markdown(st.session_state.results[skill.id])
                
                # Download Button for each
                st.download_button(
                    label=f"Download {skill.name}",
                    data=st.session_state.results[skill.id],
                    file_name=f"skill_{skill.id}_output.md",
                    mime="text/markdown"
                )
            else:
                st.info("Run the analysis to see results.")

# Export All
if len(st.session_state.results) > 0:
    st.sidebar.markdown("---")
    full_report = f"# TRIZ Analysis Report\n\nOriginal Input:\n{user_input}\n\n"
    for skill in SKILLS:
        if skill.id in st.session_state.results:
            full_report += f"## {skill.name}\n\n{st.session_state.results[skill.id]}\n\n---\n\n"
            
    st.sidebar.download_button(
        label="📥 Download Full Report",
        data=full_report,
        file_name="TRIZ_Full_Report.md",
        mime="text/markdown"
    )
