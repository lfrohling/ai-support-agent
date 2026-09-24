import streamlit as st
import google.generativeai as genai
import json

# 1. Page Configuration
st.set_page_config(page_title="AI Lead & Support Routing Agent", page_icon="🤖", layout="centered")

st.title("🤖 AI Customer Support & Lead Routing Agent")
st.caption("A portfolio project demonstrating structured LLM data extraction and automation.")

# 2. Secure API Key Access
# In production, Streamlit Secrets handles this securely.
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.warning("⚠️ Please configure your GEMINI_API_KEY in the Streamlit Secrets manager.")
    st.stop()

# Configure the SDK
genai.configure(api_key=api_key)

# 3. Define the Agent Logic
def process_ticket(ticket_text):
    # System instructions force the model to behave purely as a data-extraction backend
    system_instruction = (
        "You are an enterprise customer support triage backend. Analyze the incoming text "
        "and return a raw JSON object with these EXACT keys: "
        "'sentiment' (Positive/Neutral/Negative), 'urgency' (High/Medium/Low), "
        "'category' (Technical Support/Billing/Sales Lead/General Inquiry), "
        "'summary' (A 1-sentence summary), and 'draft_reply' (A professional, highly empathetic "
        "response addressing their concern or thanking them for the lead). "
        "Do not include any markdown block formatting like ```json, just return the raw text."
    )
    
    try:
        # Using gemini-2.5-flash as it is lightning fast and cost-effective
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )
        
        response = model.generate_content(
            f"Analyze this incoming communication:\n\n{ticket_text}",
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Parse output securely
        return json.loads(response.text)
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# 4. Interactive Frontend User Interface
st.write("### Try it Out")
user_input = st.text_area(
    "Paste a sample customer email or potential business lead below:",
    placeholder="Example: Hi, I love your product but our billing department got charged twice this month. Please fix ASAP or we will cancel our subscription. Thanks, Sarah from Enterprise Corp.",
    height=150
)

if st.button("Process & Route Communication", type="primary"):
    if not user_input.strip():
        st.error("Please provide some text to analyze.")
    else:
        with st.spinner("Analyzing text, extracting metadata, and drafting response..."):
            result = process_ticket(user_input)
            
            if result:
                st.success("Analysis Complete!")
                
                # Create visual blocks for extracted metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🚨 Urgency", result.get("urgency", "N/A"))
                with col2:
                    st.metric("🎭 Sentiment", result.get("sentiment", "N/A"))
                with col3:
                    st.metric("📁 Target Department", result.get("category", "N/A"))
                
                # Display textual results
                st.write("---")
                st.subheader("📝 Executive Summary")
                st.write(result.get("summary", ""))
                
                st.subheader("✉️ Automated Draft Response")
                st.info(result.get("draft_reply", ""))
