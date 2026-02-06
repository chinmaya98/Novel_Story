import streamlit as st
import os
import base64
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="The Geometry of Us", page_icon="💖", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'page' not in st.session_state:
    st.session_state.page = "landing"

# --- HELPER: BASE64 IMAGES ---
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# --- ENHANCED CSS: MAP BACKGROUND ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Playfair+Display:ital,wght@0,700;1,400&family=Lato:wght@300;400;700&display=swap');
    
    .stApp {{
        /* Background Map Layer + Animated Gradient */
        background: 
            linear-gradient(rgba(231, 60, 126, 0.7), rgba(35, 166, 213, 0.7)),
            url('https://www.transparenttextures.com/patterns/world-map.png'); /* Subtle map texture */
        background-size: cover;
        background-attachment: fixed;
    }}

    .bday-header {{ 
        font-family: 'Dancing Script', cursive; 
        font-size: 6.5rem; 
        color: white; 
        text-align: center; 
        text-shadow: 4px 4px 15px rgba(0,0,0,0.4);
    }}

    .reason-card {{
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        color: white;
        font-family: 'Playfair Display', serif;
        font-size: 1.6rem;
        text-align: center;
        margin: 20px auto;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}

    .card-container {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        transition: all 0.4s ease-in-out;
        border-top: 10px solid;
        height: 440px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- THE SHARED LINK ---
GEMINI_LINK = "https://gemini.google.com/share/ef6f607ddf18"

# --- PAGE 1: THE SURPRISE LANDING ---
if st.session_state.page == "landing":
    st.balloons()
    st.snow()
    
    st.markdown("<h1 class='bday-header'>Happy Birthday, Abhi!</h1>", unsafe_allow_html=True)

    # Visualizing the flight path across the world
    

    # --- SECTION 1: OUR STATS ---
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Days of Love", "2,922")
    with col2: st.metric("Continents", "2")
    with col3: st.metric("USA States", "3")
    with col4: st.metric("Shared Future", "1")

    # --- SECTION 2: THE REASON GENERATOR ---
    st.write("---")
    st.markdown("<h3 style='text-align:center; color:white;'>💌 Why Every Day Counts</h3>", unsafe_allow_html=True)
    
    reasons = [
        "Because you know the exact brand of chocolates to bring me when I'm sick.",
        "Because you taught me I don't need headphones to find peace.",
        "Because you're the only routine I ever truly wanted to keep.",
        "Because you crossed an ocean, and I followed.",
        "Because you are my geography—the map I use to navigate the world.",
        "Because with you, I lived a life composed entirely of 'firsts'.",
        "Because you make me feel like the absolute center of your universe.",
        "Because you are the silent architect of my confidence."
    ]

    _, mid_btn, _ = st.columns([1,1,1])
    with mid_btn:
        if st.button("❤️ Reveal a Reason", use_container_width=True):
            st.session_state.current_reason = random.choice(reasons)
    
    if 'current_reason' in st.session_state:
        st.markdown(f"""<div class="reason-card">"{st.session_state.current_reason}"</div>""", unsafe_allow_html=True)

    # --- TRANSITION ---
    st.write("---")
    _, enter_col, _ = st.columns([1,1,1])
    with enter_col:
        if st.button("🎁 OPEN THE GEOMETRY VAULT", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

# --- PAGE 2: AUTHENTICATION ---
elif st.session_state.page == "login":
    st.markdown("<h2 style='text-align: center; color: white; margin-top: 100px;'>🔒 Access Protected</h2>", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1,1])
    with col:
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password (Tara2018)", type="password")
            if st.form_submit_button("Unlock"):
                if u.lower() == "abhi" and p == "Tara2018":
                    st.session_state.authenticated = True
                    st.session_state.page = "gallery"
                    st.rerun()
                else:
                    st.error("Incorrect key.")

# --- PAGE 3: THE GALLERY ---
elif st.session_state.page == "gallery":
    if not st.session_state.authenticated:
        st.session_state.page = "login"
        st.rerun()

    st.markdown("<h1 style='text-align:center; color:white;'>📍 Our Journey Map</h1>", unsafe_allow_html=True)
    
    # A visual timeline of the locations mentioned in the story
    

    phases = [
        ("Phase I", "The Bonfire", "#FF6B6B", "bonfire.jpg"),
        ("Phase II", "The Great Pause", "#4ECDC4", "lockdown.jpg"),
        ("Phase III", "The Great Leap", "#F7D794", "leap.jpg"),
        ("Phase IV", "The Cold Breeze", "#A29BFE", "arrival.jpg"),
        ("Phase V", "San Jose", "#55E6C1", "san_jose.jpg"),
        ("Phase VI", "Tara's 25th", "#FD79A8", "birthday.jpg"),
        ("Phase VII", "Texas & Seattle", "#FAB1A0", "seattle.jpg"),
        ("Phase VIII", "Reality of Now", "#00CEC9", "now.jpg"),
        ("Final", "Always Yours", "#6C5CE7", "letter.jpg")
    ]

    cols = st.columns(3)
    for i, (p_id, title, color, img_file) in enumerate(phases):
        img_b64 = get_image_base64(f"images/{img_file}")
        img_src = f"data:image/jpeg;base64,{img_b64}" if img_b64 else f"https://via.placeholder.com/400x240/{color.replace('#','')}/ffffff?text={title}"
        with cols[i % 3]:
            st.markdown(f"""
                <a href="{GEMINI_LINK}" target="_blank" style="text-decoration:none;">
                    <div class="card-container" style="border-top-color: {color}">
                        <img src="{img_src}" style="width:100%; height:240px; object-fit:cover;">
                        <div style="padding:20px;">
                            <h4 style="color:{color};">{p_id}</h4>
                            <h2 style="color:#2c3e50; font-size:1.5rem;">{title}</h2>
                        </div>
                    </div>
                </a>
            """, unsafe_allow_html=True)

    if st.button("🔙 Logout"):
        st.session_state.authenticated = False
        st.session_state.page = "landing"
        st.rerun()