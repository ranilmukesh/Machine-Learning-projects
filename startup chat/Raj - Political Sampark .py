import streamlit as st
import google.generativeai as genai
import os
from pathlib import Path

# Theme configuration
def set_theme(is_dark_mode):
    if is_dark_mode:
        st.markdown("""
            <style>
                /* Main app background */
                .stApp {
                    background-color: #0E1117;
                    color: #FAFAFA;
                }
                
                /* Sidebar */
                section[data-testid="stSidebar"] {
                    background-color: #262730;
                    border-right: 1px solid #4B4B4B;
                }
                
                /* Radio buttons in sidebar */
                .stRadio > div {
                    color: #FAFAFA !important;
                }
                .stRadio > div > div > label {
                    color: #FAFAFA !important;
                }
                .stRadio > div > div > label > div {
                    background-color: #4B4B4B !important;
                    border: 2px solid #FAFAFA !important;
                }
                .stRadio > div > div > label:hover {
                    background-color: #363940 !important;
                }
                
                /* Sidebar title */
                [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
                    color: #FAFAFA !important;
                    padding: 1rem 0;
                }
                
                /* Buttons */
                .stButton>button {
                    color: #FAFAFA;
                    background-color: #262730;
                    border: 1px solid #4B4B4B;
                }
                
                /* Text inputs */
                .stTextInput>div>div>input {
                    color: #FAFAFA !important;
                    background-color: #262730 !important;
                    border-color: #4B4B4B !important;
                }
                
                /* Select boxes */
                .stSelectbox>div>div>select {
                    color: #FAFAFA !important;
                    background-color: #262730 !important;
                    border-color: #4B4B4B !important;
                }
                
                /* Text areas */
                .stTextArea>div>div>textarea {
                    color: #FAFAFA !important;
                    background-color: #262730 !important;
                    border-color: #4B4B4B !important;
                }
                
                /* Code blocks */
                .stCodeBlock {
                    background-color: #1E1E1E !important;
                    border-color: #4B4B4B !important;
                }
                
                /* Success/Info/Warning/Error boxes */
                .stAlert {
                    background-color: #262730;
                    color: #FAFAFA;
                    border: 1px solid #4B4B4B;
                }
                
                /* Form container */
                .stForm {
                    background-color: #1E1E1E;
                    padding: 1rem;
                    border-radius: 5px;
                    border: 1px solid #4B4B4B;
                }
                
                /* Spinner */
                .stSpinner > div {
                    border-color: #FAFAFA !important;
                }
                
                /* Headers */
                h1, h2, h3 {
                    color: #FAFAFA !important;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                /* Main app background */
                .stApp {
                    background-color: #FFFFFF;
                    color: #262730;
                }
                
                /* Sidebar */
                section[data-testid="stSidebar"] {
                    background-color: #F0F2F6;
                    border-right: 1px solid #E0E0E0;
                }
                
                /* Radio buttons in sidebar */
                .stRadio > div {
                    color: #262730 !important;
                }
                .stRadio > div > div > label {
                    color: #262730 !important;
                }
                .stRadio > div > div > label > div {
                    background-color: #FFFFFF !important;
                    border: 2px solid #262730 !important;
                }
                .stRadio > div > div > label:hover {
                    background-color: #E6E6E6 !important;
                }
                
                /* Sidebar title */
                [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
                    color: #262730 !important;
                    padding: 1rem 0;
                }
                
                /* Buttons */
                .stButton>button {
                    color: #262730;
                    background-color: #FFFFFF;
                    border: 1px solid #E0E0E0;
                }
                
                /* Text inputs */
                .stTextInput>div>div>input {
                    color: #262730 !important;
                    background-color: #FFFFFF !important;
                    border-color: #E0E0E0 !important;
                }
                
                /* Select boxes */
                .stSelectbox>div>div>select {
                    color: #262730 !important;
                    background-color: #FFFFFF !important;
                    border-color: #E0E0E0 !important;
                }
                
                /* Text areas */
                .stTextArea>div>div>textarea {
                    color: #262730 !important;
                    background-color: #FFFFFF !important;
                    border-color: #E0E0E0 !important;
                }
                
                /* Code blocks */
                .stCodeBlock {
                    background-color: #F8F9FA !important;
                    border-color: #E0E0E0 !important;
                }
                
                /* Success/Info/Warning/Error boxes */
                .stAlert {
                    background-color: #F8F9FA;
                    color: #262730;
                    border: 1px solid #E0E0E0;
                }
                
                /* Form container */
                .stForm {
                    background-color: #FFFFFF;
                    padding: 1rem;
                    border-radius: 5px;
                    border: 1px solid #E0E0E0;
                }
                
                /* Headers */
                h1, h2, h3 {
                    color: #262730 !important;
                }
            </style>
        """, unsafe_allow_html=True)

# Set up configuration
if not os.path.exists(".streamlit"):
    os.makedirs(".streamlit")

# Theme selection in sidebar with custom styling
with st.sidebar:
    st.markdown('<h1 style="margin-bottom: 2rem;">⚙️ Settings</h1>', unsafe_allow_html=True)
    theme_mode = st.radio(
        "Choose Theme",
        ["Light Mode 🌞", "Dark Mode 🌙"],
        index=1 if st.session_state.get('dark_mode', True) else 0
    )
    st.session_state['dark_mode'] = theme_mode == "Dark Mode 🌙"

# Apply theme
set_theme(st.session_state['dark_mode'])


# Configure Gemini API
genai.configure(api_key="AIzaSyBW-dTiQGvyAw7bpAEYsT4mPvcx6WWB4p0")
model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')

def call_gemini_api(prompt: str) -> str:
    try:
        response = model.generate_content(prompt, stream=True)
        
        # Initialize an empty string to store the complete response
        full_response = ""
        
        # Create a placeholder for the streaming response
        response_placeholder = st.empty()
        
        # Stream the response
        for chunk in response:
            if chunk.text:
                full_response += chunk.text
                # Update the placeholder with the accumulated response
                response_placeholder.markdown(full_response)
        
        return full_response
    except Exception as e:
        st.error(f"Error calling Gemini API: {str(e)}")
        return "API call failed."

# --- Streamlit App UI ---
st.title("Startup Fundraising Prompt Generator")
st.write("Choose one of the two modes below to generate a custom fundraising prompt:")

# Mode selection
mode = st.radio("Select Prompt Mode:", options=["Preset Mode", "Custom Mode"], horizontal=True)

if mode == "Preset Mode":
    st.subheader("Preset Prompt Generator")
    with st.form("preset_form"):
        # Required fields
        stage = st.selectbox("Startup Stage", options=["Pre-seed", "Seed", "Series A", "Series B+"])
        industry = st.text_input("Industry (e.g., SaaS, Fintech, HealthTech)", placeholder="Enter your industry")
        investor_type = st.selectbox("Target Investors", options=["Angel Investors", "Venture Capitalists", "Crowdfunding"])
        
        # Optional field
        challenge = st.text_area("Specific Challenges (optional)", 
                               help="Describe any specific issues you are facing, e.g., pitch deck, valuation concerns.",
                               placeholder="No specific challenges mentioned")
        
        preset_submitted = st.form_submit_button("Generate Preset Prompt")

    if preset_submitted:
        # Validate required fields
        if not industry.strip():
            st.warning("Please fill in the Industry field")
            st.stop()
            
        # Build the prompt
        challenge_text = challenge if challenge.strip() else "No specific challenges mentioned"
        preset_prompt = (
            f"As an expert startup fundraising advisor, how should a {industry.strip()} startup "
            f"at the {stage} stage approach {investor_type}? "
            f"Address these specific challenges: {challenge_text}. "
            "Provide actionable strategies and common pitfalls to avoid. "
            "Format your response in markdown with clear headings and bullet points where appropriate."
        )

        # Display and process
        st.subheader("Crafted Preset Prompt")
        st.code(preset_prompt, language="text")

        with st.spinner("Generating response with Gemini..."):
            preset_reply = call_gemini_api(preset_prompt)
            
        st.subheader("Generated Response")
        st.markdown(preset_reply)
        st.success("Preset prompt generation complete!")

elif mode == "Custom Mode":
    st.subheader("Custom Prompt Generator")
    with st.form("custom_form"):
        custom_prompt = st.text_area("Enter your custom prompt below:", 
                                   height=150,
                                   placeholder="e.g., 'How to negotiate valuation with Series A investors in AI space?'",
                                   help="Type any fundraising-related prompt you need help with.")
        custom_submitted = st.form_submit_button("Generate Custom Prompt")

    if custom_submitted:
        if not custom_prompt.strip():
            st.warning("Please enter a custom prompt")
            st.stop()

        st.subheader("Your Custom Prompt")
        st.code(custom_prompt, language="text")

        with st.spinner("Generating response with Gemini..."):
            custom_reply = call_gemini_api(custom_prompt.strip())
            
        st.subheader("Generated Response")
        st.markdown(custom_reply)
        st.success("Custom prompt generation complete!")