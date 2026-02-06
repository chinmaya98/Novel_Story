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
if 'viewing_us_photos' not in st.session_state:
    st.session_state.viewing_us_photos = False

# --- HELPER: CACHED BASE64 IMAGES (SPEED OPTIMIZATION) ---
@st.cache_data
def get_image_base64(path):
    """Reads image once and stores in RAM to prevent slow loading."""
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# --- DYNAMIC STYLING ---
def apply_custom_styles(img_filename):
    bin_str = get_image_base64(f"images/{img_filename}")
    if bin_str:
        st.markdown(f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Playfair+Display:ital,wght@0,700;1,400&display=swap');
            [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{ background-color: transparent !important; }}
            .stApp {{
                background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("data:image/png;base64,{bin_str}");
                background-size: cover; background-position: center; background-attachment: fixed;
            }}
            h1, h2, h3, p, [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{
                color: white !important; text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
            }}
            .stButton>button {{
                background: rgba(255, 255, 255, 0.15) !important;
                backdrop-filter: blur(10px) !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                color: white !important; border-radius: 15px !important;
                transition: 0.3s ease !important;
            }}
            .stButton>button:hover {{ background: rgba(255, 255, 255, 0.3) !important; transform: scale(1.02) !important; }}
            .photo-card {{ border: 4px solid white; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 20px rgba(0,0,0,0.3); }}
            </style>
            """, unsafe_allow_html=True)

GEMINI_LINK = "https://gemini.google.com/share/ef6f607ddf18"

# --- PAGE 1: LANDING ENTRANCE ---
if st.session_state.page == "landing":
    apply_custom_styles("map.png")
    st.balloons()
    st.markdown("<h1 style='font-family:\"Dancing Script\", cursive; font-size: 6rem; text-align: center;'>Happy Birthday, Abhi!</h1>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Days of Love", "2,922")
    with col2: st.metric("Continents", "2")
    with col3: st.metric("Cities Together", "12+")
    with col4: st.metric("Shared Future", "1")

    st.write("---")
    _, heart_col, _ = st.columns([1,1,1])
    with heart_col:
        if st.button("❤️ Reveal a Reason", use_container_width=True):
            reasons = ["Because you crossed an ocean, and I followed.", "Because you are my geography.", "Because you are the silent architect of my confidence."]
            st.session_state.current_reason = random.choice(reasons)
            st.snow()
    
    if 'current_reason' in st.session_state:
        st.markdown(f'<div style="background:rgba(255,255,255,0.2); backdrop-filter:blur(15px); border-radius:30px; padding:30px; text-align:center;"><p style="font-size:1.5rem;">"{st.session_state.current_reason}"</p></div>', unsafe_allow_html=True)

    st.write("##")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("📁 OPEN PHOTO SUB-FOLDERS", use_container_width=True):
            st.session_state.page = "photo_categories"
            st.rerun()
        if st.button("🎁 UNLOCK THE STORYBOOK", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

# --- PAGE 2: PUBLIC PHOTOS ---
elif st.session_state.page == "photo_categories":
    apply_custom_styles("backcover.png")
    st.markdown("<h1 style='text-align:center;'>Memory Vault</h1>", unsafe_allow_html=True)
    
    categories = {"Friends": "friends", "Places": "place", "Food": "food"}
    cols = st.columns(len(categories))
    for i, (name, prefix) in enumerate(categories.items()):
        with cols[i]:
            if st.button(name, use_container_width=True):
                st.session_state.selected_category = prefix

    if st.session_state.selected_category:
        folder, prefix = "gallery", st.session_state.selected_category
        if os.path.exists(folder):
            cat_photos = [f for f in os.listdir(folder) if f.startswith(prefix)]
            grid_cols = st.columns(3)
            for idx, photo in enumerate(cat_photos):
                with grid_cols[idx % 3]:
                    img_b64 = get_image_base64(os.path.join(folder, photo))
                    st.markdown(f'<div class="photo-card"><img src="data:image/jpeg;base64,{img_b64}" style="width:100%; height:250px; object-fit:cover;"></div>', unsafe_allow_html=True)

    if st.button("🔙 Back Home"): st.session_state.page = "landing"; st.rerun()

# --- PAGE 3: LOGIN ---
elif st.session_state.page == "login":
    apply_custom_styles("backcover.png")
    st.markdown("<h2 style='text-align: center; margin-top: 100px;'>🔒 Access Protected</h2>", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1,1])
    with col:
        with st.form("auth"):
            u = st.text_input("Username")
            p = st.text_input("Secret Key (Tara2018)", type="password")
            if st.form_submit_button("Access Vault"):
                if u.lower() == "abhi" and p == "Tara2018":
                    st.session_state.authenticated = True
                    st.session_state.page = "gallery"
                    st.rerun()
                else: st.error("Incorrect Key.")
    if st.button("Back"): st.session_state.page = "landing"; st.rerun()

# --- PAGE 4: THE JOURNEY VAULT (PRIVATE) ---
# --- PAGE 4: THE JOURNEY VAULT (PRIVATE) ---
elif st.session_state.page == "gallery":
    if not st.session_state.authenticated: 
        st.session_state.page = "login"; st.rerun()
    
    apply_custom_styles("map.png")
    st.markdown("<h1 style='text-align:center;'>📐 Our Journey Vault</h1>", unsafe_allow_html=True)

    # --- SUB-PAGE: PRIVATE MOMENTS REEL ---
    if st.session_state.get('viewing_us_photos', False):
        st.markdown("<h1 style='text-align:center;'>❤️ Our Private Moments</h1>", unsafe_allow_html=True)
        if st.button("🔙 Back to Journey Phases"): 
            st.session_state.viewing_us_photos = False; st.rerun()
        
        st.write("---")
        folder = "gallery"
        if os.path.exists(folder):
            us_photos = [f for f in os.listdir(folder) if f.startswith("us_")]
            if us_photos:
                grid_cols = st.columns(3)
                for idx, photo in enumerate(us_photos):
                    with grid_cols[idx % 3]:
                        img_b64 = get_image_base64(os.path.join(folder, photo))
                        st.markdown(f'<div class="photo-card"><img src="data:image/jpeg;base64,{img_b64}" style="width:100%; height:250px; object-fit:cover;"></div>', unsafe_allow_html=True)
    
    # --- MAIN VIEW: ALIGNED PHASE CARDS ---
    else:
        phase_links = {
            "Phase I": "https://gemini.google.com/share/5e0867acc937",
            "Phase II": "https://gemini.google.com/share/c87b69424443",
            "Phase III": "https://gemini.google.com/share/2d6a70e7cfb7",
            "Phase IV": "https://gemini.google.com/share/876e191d3f58",
            "Phase V": "https://gemini.google.com/share/a627741c67f6",
            "Phase VI": "https://gemini.google.com/share/ccbabe563dd0",
            "Phase VII": "https://gemini.google.com/share/f934d96cd185",
            "Phase VIII": "https://gemini.google.com/share/fa058a3d73f7",
            "Final": "https://gemini.google.com/share/ef6f607ddf18"
        }

        phases = [
            ("Vault", "The Us Vault", "#FFD700", "us_cover.png"), 
            ("Phase I", "The Bonfire", "#FF6B6B", "bonfire.png"),
            ("Phase II", "The Great Pause", "#4ECDC4", "lockdown.png"),
            ("Phase III", "The Great Leap", "#F7D794", "leap.png"),
            ("Phase IV", "The Cold Breeze", "#A29BFE", "arrival.png"),
            ("Phase V", "San Jose", "#55E6C1", "san_jose.png"),
            ("Phase VI", "Tara's 25th", "#FD79A8", "birthday.png"),
            ("Phase VII", "Texas & Seattle", "#FAB1A0", "seattle.png"),
            ("Phase VIII", "Reality of Now", "#00CEC9", "now.png"),
            ("Final", "Always Yours", "#6C5CE7", "letter.png")
        ]
        
        cols = st.columns(3)
        for i, (p_id, title, color, img_file) in enumerate(phases):
            with cols[i % 3]:
                img_b64 = get_image_base64(f"images/{img_file}")
                
                # We use a single div structure for EVERYTHING to ensure alignment
                card_html = f"""
                    <div style="background:rgba(255,255,255,0.95); border-radius:20px; overflow:hidden; border-top:10px solid {color}; text-align:center; color:#2c3e50; height: 350px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                        <img src="data:image/png;base64,{img_b64}" style="width:100%; height:200px; object-fit:cover;">
                        <div style="padding:15px;">
                            <h4 style="color:{color}; margin:0;">{p_id}</h4>
                            <h3 style="margin:5px 0; color:#2c3e50;">{title}</h3>
                """

                if p_id == "Vault":
                    # For the Vault, the card contains an internal button
                    st.markdown(card_html + "</div></div>", unsafe_allow_html=True)
                    if st.button(f"🔓 Open {title}", key="v_btn_final", use_container_width=True):
                        st.session_state.viewing_us_photos = True; st.balloons(); st.rerun()
                else:
                    # For Phases, the whole card is a link
                    link = phase_links.get(p_id, GEMINI_LINK)
                    full_card = f"""
                        <a href="{link}" target="_blank" style="text-decoration:none;">
                            {card_html}
                            <p style="font-size:0.8rem; color:#666;">📖 Read Our Story</p>
                        </div></a>
                    """
                    st.markdown(full_card, unsafe_allow_html=True)

    if st.button("🔙 Back Home"):
        st.session_state.authenticated = False; st.session_state.page = "landing"; st.rerun()