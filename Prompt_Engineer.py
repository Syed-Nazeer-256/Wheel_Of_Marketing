import streamlit as st
import google.generativeai as genai
import os
import time
import random

GEMINI_API_KEY = "AIzaSyD1WeVGIKaV1oyYlDsk2a_EDWdsSclwMqU"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')  # Use flash model for higher free tier limits

# Custom CSS for fluid animations and dark theme
st.markdown("""
<style>
body {
    background-color: #1e1e2e;
    color: #cdd6f4;
}
.stButton>button {
    background: linear-gradient(45deg, #6b48ff, #00ddeb);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 4px 15px rgba(107, 72, 255, 0.4);
}
.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(107, 72, 255, 0.6);
}
.stTextInput>div>input, .stSelectbox>div>select {
    background-color: #2a2a3b;
    color: #cdd6f4;
    border-radius: 8px;
    border: 1px solid #44475a;
    padding: 10px;
    transition: border-color 0.3s ease;
}
.stTextInput>div>input:focus, .stSelectbox>div>select:focus {
    border-color: #6b48ff;
    box-shadow: 0 0 8px rgba(107, 72, 255, 0.3);
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in {
    animation: fadeIn 0.5s ease-in;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.spinner {
    border: 4px solid #44475a;
    border-top: 4px solid #6b48ff;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
}
.output-box {
    background-color: #2a2a3b;
    border-radius: 12px;
    padding: 20px;
    margin-top: 20px;
    border: 1px solid #44475a;
    animation: fadeIn 0.5s ease-in;
}
h1, h2, h3 {
    color: #cdd6f4;
    text-shadow: 0 2px 4px rgba(107, 72, 255, 0.2);
}
.error-box {
    background-color: #3b2a2a;
    border: 1px solid #ff5555;
    border-radius: 8px;
    padding: 15px;
    margin-top: 20px;
    color: #ffcccc;
    animation: fadeIn 0.5s ease-in;
}
</style>
""", unsafe_allow_html=True)

# Streamlit app title and description
st.title("✨ Awesome Prompt Generator")
st.markdown("Craft golden-standard prompts with ease! Customize tone, domain, and complexity, powered by Gemini API.")

# Input form for prompt parameters
with st.form("prompt_form"):
    st.subheader("Customize Your Prompt")
    tone = st.selectbox("Select Tone", ["Professional", "Creative", "Casual", "Formal", "Persuasive"])
    domain = st.selectbox("Select Domain", ["Writing", "Programming", "Marketing", "Education", "Storytelling", "Other"])
    complexity = st.selectbox("Complexity Level", ["Simple", "Moderate", "Detailed", "Expert"])
    custom_instructions = st.text_area("Additional Instructions (optional)", placeholder="E.g., 'Include examples' or 'Focus on sci-fi themes'")
    submitted = st.form_submit_button("Generate Prompt")

# Function to generate prompt using Gemini API with retry logic
def generate_prompt(tone, domain, complexity, custom_instructions, max_retries=3):
    for attempt in range(max_retries):
        try:
            prompt_template = f"""
            You are an expert prompt engineer tasked with creating a golden-standard, highly detailed, and creative prompt. 
            Craft a prompt with the following specifications:
            - Tone: {tone}
            - Domain: {domain}
            - Complexity: {complexity}
            - Additional Instructions: {custom_instructions if custom_instructions else 'None'}
            The prompt should be clear, engaging, and optimized for generating high-quality responses. 
            Include specific guidance, context, and examples where relevant. 
            Return the prompt in a concise yet comprehensive format, suitable for immediate use.
            """
            response = model.generate_content(prompt_template)
            return response.text, None
        except Exception as e:
            if "429" in str(e):
                retry_delay = 41 + random.uniform(0, 5)  # Base delay from error + jitter
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return None, "Error: Exceeded Gemini API rate limits. Please check your plan and billing details at https://ai.google.dev/gemini-api/docs/rate-limits or wait 41 seconds before retrying."
            return None, f"Error generating prompt: {str(e)}"

# Handle form submission
if submitted:
    # Show loading spinner
    with st.spinner(""):
        placeholder = st.empty()
        placeholder.markdown('<div class="spinner"></div>', unsafe_allow_html=True)
        prompt_result, error_message = generate_prompt(tone, domain, complexity, custom_instructions)
        placeholder.empty()
    
    # Display result or error
    if error_message:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.error(error_message)
        if "rate limits" in error_message:
            st.markdown("**Solution**: Upgrade to a paid tier in Google AI Studio by setting up a billing account for higher rate limits. Visit [Gemini API Pricing](https://ai Grok: .google.dev/pricing) for details.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="output-box">', unsafe_allow_html=True)
        st.subheader("Generated Prompt")
        st.write(prompt_result)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Gemini API")
