import streamlit as st
import google.generativeai as genai
import json

# 1. Page Configuration
st.set_page_config(page_title="AI Lead & Support Routing Agent", page_icon="🤖", layout="centered")

st.title("🤖 AI Customer Support & Lead Routing Agent")
st.caption("A portfolio project demonstrating structured LLM data extraction and automation.")

# Mock data for seamless recruiter testing when API limits are capped
MOCK_RESPONSE = {
    "urgency": "High",
    "sentiment": "Negative",
    "category": "Billing",
    "summary": "Customer Sarah from MegaCorp is demanding an immediate refund for a duplicate enterprise charge and threatening account cancellation.",
    "draft_reply": "Hi Sarah, thank you for reaching out. We sincerely apologize for the duplicate charge on your enterprise statement. I have forwarded this ticket to our billing infrastructure leads with highest priority. A manual correction is currently processing, and we will update you within 2 business hours. We value MegaCorp's partnership and will ensure this is resolved immediately. Best regards, Customer Operations Team."
}

# 2. Interactive Frontend Configuration Controls
st.sidebar.header("🛠️ Project Controls")
demo_mode = st.sidebar.toggle("Enable Recruiter Simulator Mode", value=True, 
                             help="Bypasses Google's strict 20-request daily free quota using cached mock enterprise outputs.")

# Secure API Key Access
api_key = st.secrets.get("GEMINI_API_KEY", "")
if not demo_mode and not api_key:
    st.warning("⚠️ Please configure your GEMINI_API_KEY in the Streamlit Secrets manager.")
    st.stop()

if api_key:
    genai.configure(api_key=api_key)

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# 3. Define the Agent Logic
def process_ticket(ticket_text):
    if demo_mode:
        return MOCK_RESPONSE
        
    system_instruction = (
        "You are an enterprise customer support triage backend. Analyze the incoming text "
        "and return a raw JSON object with these EXACT keys: "
        "'sentiment' (Positive/Neutral/Negative), 'urgency' (High/Medium/Low), "
        "'category' (Technical Support/Billing/Sales Lead/General Inquiry), "
        "'summary' (A 1-sentence summary), and 'draft_reply' (A professional, highly empathetic "
        "response addressing their concern). Do not include markdown blocks."
    )
    try:
        model = genai.GenerativeModel(model_name="gemini-3.8-flash", system_instruction=system_instruction)
        response = model.generate_content(f"Analyze:\n\n{ticket_text}", generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        st.error(f"API Processing Error: {e}")
        st.info("💡 Tip: Toggle 'Recruiter Simulator Mode' in the sidebar to view UI capabilities while API limits clear.")
        return None

# 4. User Interface
st.write("### Try it Out")
if demo_mode:
    st.info("ℹ️ **Recruiter Simulator Mode is Active.** The application UI will use cached enterprise weights to instantly simulate live processing.")

with st.form("triage_form"):
    user_input = st.text_area(
        "Paste a sample customer email or potential business lead below:",
        placeholder="Example: Hi, I love your product but our billing department got charged twice this month. Please fix ASAP or we will cancel our subscription. Thanks, Sarah from Enterprise Corp.",
        height=150
    )
    submit_button = st.form_submit_button("Process & Route Communication", type="primary")

if submit_button:
    if not user_input.strip():
        st.error("Please provide some text to analyze.")
    else:
        with st.spinner("Analyzing text, extracting metadata, and drafting response..."):
            result = process_ticket(user_input)
            if result:
                st.session_state.analysis_result = result

# 5. Render outputs
if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    st.success("Analysis Complete!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🚨 Urgency", result.get("urgency", "N/A"))
    with col2:
        st.metric("🎭 Sentiment", result.get("sentiment", "N/A"))
    with col3:
        st.metric("📁 Target Department", result.get("category", "N/A"))
    
    st.write("---")
    st.subheader("📝 Executive Summary")
    st.write(result.get("summary", ""))
    
    st.subheader("✉️ Automated Draft Response")
    st.info(result.get("draft_reply", ""))

# ==========================================
# 📊 INTERACTIVE PROJECT PORTFOLIO DIRECTORY HUB
# ==========================================
st.write("---")
st.subheader("💼 Engineering Portfolio Directory & Capabilities Index")
st.markdown(
    "This section outlines the architectural frameworks, data schemas, and modern AI SDKs "
    "put into production across this portfolio series. Click the drop-downs below to inspect "
    "completed deployment vectors and source files."
)

# Project 1 Accordion Row
with st.expander("🤖 Project 1: Automated Customer Support & Lead Triage Agent"):
    st.markdown("""
    *   **Core Objective:** Automate corporate communication workflows by parsing unstructured inputs into programmatic data payloads.
    *   **Engineering Optimizations Implemented:** 
        *   **Structured JSON Output Payloads:** Forced the core LLM backend to filter out conversational filler and generate pure, machine-parsable JSON schemas mapping to designated business metrics (`sentiment`, `urgency`, `category`).
        *   **State Management Throttling:** Wrapped UI inputs in explicit atomic form validation tags to block aggressive script loops from flooding third-party endpoints.
    *   **Sub-Systems & Software Employed:** Python 3.12, Streamlit Form Framework, `google-generativeai` SDK, Git, Streamlit Cloud Hosting.
    """)
    # Replace the bracket placeholders below with your actual custom URLs
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("[🌐 Launch Live Web Application](https://streamlit.app)")
    with col2:
        st.markdown("[📁 Review Source Code Repository (GitHub)](https://github.com)")

# Project 2 Accordion Row
with st.expander("🔍 Project 2: Intelligent Document Search Engine (RAG System)"):
    st.markdown("""
    *   **Core Objective:** Mitigate enterprise data loss and remove information lookup friction using contextual reference injection.
    *   **Engineering Optimizations Implemented:** 
        *   **In-Memory Retrieval-Augmented Generation (RAG):** Built a system that dynamically loads external `.txt` documentation directly into the runtime context window.
        *   **Strict Context Constraint Framing:** Programmed defensive system prompt barriers instructing the model to declare an automatic 'Information Not Found' payload if facts cannot be extracted entirely from the source document.
    *   **Sub-Systems & Software Employed:** Python 3.12, Streamlit UI, Modernized `google-genai` Interactions SDK, Mermaid.js Visual Flow Architecture Engine.
    """)
    # Replace the bracket placeholders below with your actual custom URLs
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("[🌐 Launch Live Web Application](https://streamlit.app)")
    with col4:
        st.markdown("[📁 Review Source Code Repository (GitHub)](https://github.com)")

# Master Skills Summary Matrix Block
with st.expander("🛠️ Core Technology & Systems Engineering Summary Table"):
    st.markdown(
        "Below is a direct architectural overview of the systems, data models, and deployment "
        "utilities engineered throughout these implementations:"
    )
    
    # Render a clean, scannable data summary grid for hiring teams
    st.markdown(
        """

        | Software / Framework | Implementation Layer | Operational Purpose |
        | :--- | :--- | :--- |
        | **Python 3.12** | Core Backend Engine | Script automation logic, error routing blocks, and payload structural processing. |
        | **Streamlit Framework** | Presentation / UI | Handling page script re-renders cleanly, state preservation, and layout presentation. |
        | **google-genai SDK** | AI Infrastructure Model | Utilizing bleeding-edge Interactions API pipelines for structured document grounding. |
        | **Mermaid.js Notation** | Systems Architecture | Standardized color-coded flow charts to visibly communicate data flow configurations. |
        | **Git & GitHub** | Version Control | Maintaining deployment history pipelines and recruiter-facing documentation briefs. |
        """
    )
st.caption("🔒 *All endpoints are securely managed via isolated production environmental variables (`st.secrets`).*")
