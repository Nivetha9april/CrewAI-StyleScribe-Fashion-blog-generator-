import streamlit as st
import os
from crew_logic.crew import run_topic_suggester, run_fashion_crew
from dotenv import load_dotenv
import time
import re

# Load env variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="StyleScribe AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Dark Fashion UI CSS + Magazine Carousel
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@300;400;500;600&display=swap');

    /* Global Vogue Light Theme */
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        background-color: #faf8f5 !important;
        color: #1a1a1a !important;
    }
    
    .stApp {
        background-color: #faf8f5;
    }

    h1, h2, h3, .stMarkdown p strong {
        font-family: 'Playfair Display', serif;
        color: #000000 !important;
    }

    /* Flyover Animations & Stars */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    @keyframes neon-glow {
        0% { text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 20px #e60073, 0 0 30px #e60073; }
        100% { text-shadow: 0 0 2px #fff, 0 0 5px #fff, 0 0 10px #e60073, 0 0 15px #e60073; }
    }

    .title-banner {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(230, 0, 115, 0.2);
        animation: float 6s ease-in-out infinite;
        position: relative;
        overflow: hidden;
        border: 1px solid #333;
    }
    
    .title-banner::before {
        content: '✨ ★ ✨';
        position: absolute;
        top: 10px;
        left: 20px;
        color: gold;
        font-size: 1.5rem;
        opacity: 0.5;
    }
    
    .title-banner h1 {
        margin-bottom: 0.5rem;
        font-size: 3rem;
        font-weight: 700;
        animation: neon-glow 1.5s ease-in-out infinite alternate;
    }
    
    .title-banner p {
        color: #b0b0b0 !important;
        font-style: italic;
        font-size: 1.2rem;
        margin-bottom: 0;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(45deg, #e60073, #ff4d4d);
        color: white !important;
        border-radius: 30px;
        padding: 0.6rem 2.5rem;
        font-weight: 600;
        border: none;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        width: 100%;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(230, 0, 115, 0.4);
    }
    
    .stButton>button:hover {
        transform: scale(1.05) translateY(-2px);
        box-shadow: 0 8px 25px rgba(230, 0, 115, 0.6);
    }
    
    .stRadio label {
        color: #e0e0e0 !important;
        font-size: 1.1rem;
    }
    
    .stTextInput>div>div>input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 10px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #e60073 !important;
        box-shadow: 0 0 10px rgba(230,0,115,0.4) !important;
    }

    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Poppins:wght@300;400;500;600&display=swap');

    body, .stApp {
        background: #faf8f5 !important;
        font-family: 'Poppins', sans-serif !important;
        color: #1a1a1a;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        color: #000000 !important; 
    }
    
    /* VIBRANT LAYOUT CLASSES */
    .colorful-box {
        border: 1px solid #e0e0e0;
        border-radius: 0px;
        padding: 30px;
        margin: 25px 0;
        background: #ffffff;
        box-shadow: 0 10px 40px rgba(0,0,0,0.03);
    }
    
    .slogan-box {
        background: #000000;
        color: #ffffff !important;
        padding: 40px;
        border-radius: 0px;
        text-align: center;
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-style: italic;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        margin: 50px 0;
    }
    
    .swatch-container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 15px;
        margin: 30px 0;
    }
    .swatch {
        text-align: center;
        font-size: 0.9rem;
    }
    .swatch-color {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin: 0 auto 10px auto;
        box-shadow: 0 4px 10px rgba(255,255,255,0.1);
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    .tips-container {
        display: flex;
        gap: 20px;
        justify-content: space-between;
        margin: 30px 0;
    }
    .expert-tip-card {
        flex: 1;
        background: #ffffff;
        border-top: 3px solid #1a1a1a;
        padding: 25px;
        border-radius: 0px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    .faq-box {
        background: #ffffff;
        border-left: 4px solid #1a1a1a;
        padding: 15px 20px;
        margin-bottom: 15px;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
    }
    
    .visual-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin: 30px 0;
    }
    .visual-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 0px;
        border: 1px solid #eaeaea;
        transition: transform 0.3s;
    }
    .visual-card:hover {
        transform: translateY(-5px);
        border-color: #f8e5c0;
    }
    
    .reference-container {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin: 20px 0;
    }
    .reference-pill {
        background: #f0f0f0;
        color: #1a1a1a;
        padding: 8px 18px;
        border-radius: 30px;
        text-decoration: none;
        font-size: 0.9rem;
        border: 1px solid #ddd;
        transition: background 0.3s;
    }
    .reference-pill:hover {
        background: rgba(255,255,255,0.2);
    }

    /* Scrollbar override for vertical window */
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div class="title-banner">
    <h1>✨ StyleScribe AI 🥂</h1>
    <p>"Where algorithms meet aesthetics – blog posts so stylish, even Anna Wintour would approve. 🖤"</p>
</div>
""", unsafe_allow_html=True)

# Session State Initialization
if "step" not in st.session_state:
    st.session_state.step = 1
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []
if "base_topic" not in st.session_state:
    st.session_state.base_topic = ""
# Add a key for the radio selection to persist it
if "selected_angle_radio" not in st.session_state:
    st.session_state.selected_angle_radio = None

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your_openai_api_key_here":
    st.warning("⚠️ OPENAI_API_KEY is not set or is set to the default value. Please add your key to a `.env` file.")
    st.stop()

# --- STEP 1: Enter Base Topic ---
if st.session_state.step == 1:
    st.write("### 🎬 Step 1: Give our Researcher a Topic")
    st.write("Enter ANY fashion topic (e.g., 'baggy jeans', 'office wear for summer')")
    
    base_topic_input = st.text_input("Fashion Topic 👗:")
    
    if st.button("Get Topic Ideas 💡"):
        if not base_topic_input.strip():
            st.error("Please enter a topic.")
        else:
            with st.spinner("🕵️‍♀️ Topic Strategist is brainstorming 5 unique angles..."):
                try:
                    raw_suggestions = run_topic_suggester(base_topic_input)
                    
                    # Extract titles even if the AI forgot to use newlines and put them on one line
                    parsed_suggestions = []
                    
                    # Split by newlines, or by lookahead for "1.", "2)", etc.
                    parts = re.split(r'\n|(?=\b\d+[\.\)])', raw_suggestions)
                    
                    for line in parts:
                        line = line.strip()
                        if line:
                            # Strip out the leading numbers or bullet points
                            clean_line = re.sub(r"^(?:\d+[\.\)]\s*|\-\s*|\*\s*)", "", line)
                            clean_line = clean_line.strip('\"\'') # remove surrounding quotes
                            if clean_line and len(clean_line) > 5:
                                parsed_suggestions.append(clean_line)
                    
                    if len(parsed_suggestions) < 1:
                        parsed_suggestions = [raw_suggestions]
                    
                    st.session_state.suggestions = parsed_suggestions
                    st.session_state.base_topic = base_topic_input
                    # Reset the radio selection just in case
                    st.session_state.selected_angle_radio = parsed_suggestions[0] 
                    st.session_state.step = 2
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating suggestions: {e}")

# --- STEP 2: Select Topic & Word Count ---
elif st.session_state.step == 2:
    st.write("### 💅 Step 2: Choose Your Angle & Configure")
    
    st.info(f"✨ Suggestions generated for: **{st.session_state.base_topic}**")
    
    st.markdown("---")
    st.write("### 📏 Step 3: Set Blog Guidelines")
    target_word_count = st.slider("Target Word Count (Main Content) 📝:", min_value=500, max_value=2500, value=1200, step=100)
    
    # Show an interactive button for each topic
    st.write("Click on any of the incredibly chic angles below to publish immediately!")
    for idx, suggestion in enumerate(st.session_state.suggestions):
        if st.button(f"✨ {suggestion} ✨", key=f"topic_btn_{idx}"):
            st.session_state.selected_angle_radio = suggestion
            st.session_state.step = 3
            st.session_state.target_word_count = target_word_count
            st.rerun()
            
    st.markdown("---")
    if st.button("⬅️ Start Over"):
        st.session_state.step = 1
        st.rerun()

# --- STEP 3: Execution Pipeline ---
elif st.session_state.step == 3:
    topic_to_write = st.session_state.selected_angle_radio
    st.write("### 👠 Step 4: The Fashion Scribe at Work")
    st.info(f"**Topic:** {topic_to_write}\\n**Word Count:** {st.session_state.target_word_count}")
    
    with st.status("💎 The Editorial Crew is at work...", expanded=True) as status:
        st.write("🕵️‍♀️ **Researcher** is pulling 5+ credible sources, expert quotes, and data...")
        time.sleep(1)
        st.write("🖋️ **Writer** is drafting professional, structurally exact prose out of the research...")
        time.sleep(1)
        st.write("👓 **Editor** is perfecting the HTML/Markdown layout and SEO...")
        time.sleep(1)
        st.write("🚀 Running CrewAI processes... Please wait, beauty takes time. ✨")
        
        try:
            result = run_fashion_crew(topic_to_write, st.session_state.target_word_count)
            status.update(label="Blog Post Ready! 🎉", state="complete", expanded=False)
            
            st.markdown("### 🌟 The Magazine")
            
            # Render the vertical layout directly with HTML enabled!
            st.markdown(result, unsafe_allow_html=True)
            
            st.success("Issue successfully published! 🥂")
            st.balloons()
            
            if st.button("Start New Issue 🎬"):
                st.session_state.step = 1
                st.rerun()
                
        except Exception as e:
            status.update(label="An error occurred.", state="error", expanded=True)
            st.error(f"Error during crew execution: {e}")
            if st.button("⬅️ Go Back"):
                st.session_state.step = 2
                st.rerun()
