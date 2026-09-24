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
