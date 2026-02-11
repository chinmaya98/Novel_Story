import streamlit as st
import base64
import random
import requests
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Happy Birthday", page_icon="🎁", layout="wide")

# --- GITHUB IMAGE SETTINGS ---
GITHUB_BASE_URL = "https://raw.githubusercontent.com/chinmaya98/Novel_Story/main/"

# --- 1. INITIALIZE SESSION STATE (ROBUST CLOUD VERSION) ---
initial_states = {
    'authenticated': False,
    'page': 'landing',
    'viewing_us_photos': False,
    'viewing_letter': False,
    'selected_category': None,
    'photo_index': 0,
    'current_reason': None
}

for key, value in initial_states.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- 2. HELPER: CACHED BASE64 IMAGES ---
@st.cache_data(ttl=3600)
def get_image_base64(path):
    url = path if path.startswith("http") else f"{GITHUB_BASE_URL}{path}"
    try:
        response = requests.get(url, timeout=1.5)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode()
    except: return None
    return None

# --- 3. DYNAMIC STYLING ---
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
            [data-testid="stMetric"] {{ display: flex; justify-content: center; align-items: center; text-align: center; }}
            </style>
            """, unsafe_allow_html=True)

# --- PAGE 1: LANDING ENTRANCE ---
if st.session_state.page == "landing":
    apply_custom_styles("backcover.png")
    st.balloons()
    st.markdown("<h1 style='font-family:\"Dancing Script\", cursive; font-size: 6rem; text-align: center;'>Happy Birthday, Gautam!</h1>", unsafe_allow_html=True)
    _, col1, col2, col3, _ = st.columns([1, 2, 2, 2, 1])
    with col1: st.metric("Years", "7+")
    with col2: st.metric("Continents", "2")
    with col3: st.metric("Cities Together", "12+")
        
    st.write("##")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("📁 MEMORY VAULT", use_container_width=True, key="main_vault_btn"):
            st.session_state.page = "photo_categories"; st.rerun()
        if st.button("🎁 UNLOCK THE STORYBOOK", use_container_width=True, key="main_story_btn"):
            st.session_state.page = "login"; st.rerun()

# --- PAGE 2: PUBLIC PHOTOS (MEMORY VAULT) ---
elif st.session_state.page == "photo_categories":
    apply_custom_styles("backcover.png")
    st.markdown("<h1 style='text-align:center;'>Memory Vault</h1>", unsafe_allow_html=True)
    if st.button("🔙 Back Home", key="vault_exit_back"): 
        st.session_state.page = "landing"; st.rerun()
    categories = {"Friends": "friends", "Places": "place", "Food": "food", "You": "you"}
    cols = st.columns(len(categories))
    for i, (name, prefix) in enumerate(categories.items()):
        if cols[i].button(name, key=f"nav_btn_{prefix}", use_container_width=True):
            st.session_state.selected_category = prefix; st.rerun()
    if st.session_state.selected_category:
        pref = st.session_state.selected_category
        st.write(f"### Showing: {pref.capitalize()}")
        photos = [f"{pref}_{i}.jpg" for i in range(1, 19)] 
        grid_cols = st.columns(3)
        for idx, photo in enumerate(photos):
            with grid_cols[idx % 3]:
                img_b64 = get_image_base64(f"gallery/{photo}")
                if img_b64:
                    st.markdown(f'<div class="photo-card"><img src="data:image/jpeg;base64,{img_b64}" style="width:100%; height:250px; object-fit:cover;"></div>', unsafe_allow_html=True)

# --- PAGE 3: LOGIN ---
elif st.session_state.page == "login":
    apply_custom_styles("map.png")
    st.markdown("<h2 style='text-align: center; margin-top: 100px;'>🔒 Access Protected</h2>", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1,1])
    with col:
        with st.form("auth"):
            u = st.text_input("Username")
            p = st.text_input("Secret Key", type="password")
            if st.form_submit_button("Access Vault"):
                if u.lower() in ["gautam", "gau"] and p == st.secrets["SECRET_KEY"]:
                    st.session_state.authenticated = True
                    st.session_state.page = "gallery"; st.rerun()
                else: st.error("Incorrect Key.")
    if st.button("Back", key="login_back"): st.session_state.page = "landing"; st.rerun()

# --- PAGE 4: THE JOURNEY VAULT (PRIVATE) ---
elif st.session_state.page == "gallery":
    if not st.session_state.authenticated: 
        st.session_state.page = "login"; st.rerun()
    apply_custom_styles("map.png")

    # --- SUB-PAGE: THE LETTER ---
    if st.session_state.get('viewing_letter', False):
        # 1. Back Button (Keep this OUTSIDE the HTML block)
        if st.button("🔙 Back to Journey Vault", key="final_letter_back"): 
            st.session_state.viewing_letter = False
            st.rerun()
        
        # 2. Trigger Balloons and Custom Heart Rain
        st.balloons()

        # Inject CSS for styling and Heart Animation
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Playfair+Display:wght@400;700&display=swap');
            
            .main .block-container {
                padding-top: 2rem !important;
            }
            
            .letter-box {
                background-color: #fffdf5 !important;
                padding: 50px !important;
                border-radius: 8px !important;
                border: 1px solid #e0e0e0 !important;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
                max-width: 800px;
                margin: auto;
                color: #2c3e50 !important;
                font-family: 'Playfair Display', serif !important;
                line-height: 1.8 !important;
                position: relative;
                z-index: 1;
            }
            
            .letter-box h1, .letter-box h2 {
                font-family: 'Dancing Script', cursive !important;
                color: #FF6B6B !important;
                text-shadow: none !important;
            }
            
            .letter-box p {
                color: #2c3e50 !important;
                text-shadow: none !important;
                margin-bottom: 20px !important;
                font-size: 1.1rem !important;
            }

            /* --- Heart Animation --- */
            @keyframes heartFall {
                0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
                100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
            }

            .heart-particle {
                position: fixed;
                top: -10%;
                color: #FF6B6B;
                font-size: 24px;
                user-select: none;
                z-index: 1000;
                animation: heartFall 6s linear infinite;
            }
            </style>

            <div class="heart-particle" style="left:10%; animation-delay:0s;">❤️</div>
            <div class="heart-particle" style="left:25%; animation-delay:2s;">💖</div>
            <div class="heart-particle" style="left:40%; animation-delay:1s;">💕</div>
            <div class="heart-particle" style="left:60%; animation-delay:3s;">❤️</div>
            <div class="heart-particle" style="left:75%; animation-delay:1.5s;">💗</div>
            <div class="heart-particle" style="left:90%; animation-delay:4s;">💖</div>
        """, unsafe_allow_html=True)

        # 3. Create the Letter Content
        st.markdown(r"""
        <div class="letter-box">
            <p style="text-align: right; font-weight: bold; color: #2c3e50;">February 15, 2026</p>
            <h1 style="text-align: center; color: #FF6B6B;">A Letter to the Man Who Became My Rhythm</h1>
            <h2 style="color: #FF6B6B;">Gautam,</h2>
            <p>I am sitting here with my coffee, watching the light change, and for the first time in eight years, I am trying to imagine a world where you aren’t my first thought. It’s been 2,922 days since that bonfire in the hills, and somehow, you’ve managed to become the very air I breathe without me even noticing.</p>
            <p>I wanted to tell you this today, but the words always get stuck. I want to tell you that I don’t just "value" our friendship—I am built out of it.</p>
            <p>Every version of Tara that exists today was crafted alongside you. Tara who isn’t afraid of the deep water? You did that. The Tara who moved across the globe with two suitcases and a heart full of fear? She only did it because she knew you were on the other side of that flight.</p>
            <p>I’ve spent so long worrying about the "competition"—feeling like I was the third wheel between you and Siri, or wondering if I was just the girl who fills the gaps. But looking back at the way you cared for me during my worst days... I realize now that the only person I was ever in competition with was my own fear.</p>
            <p><strong>But here is the truth that terrifies me:</strong></p>
            <p>We call this "friendship," and we wear that word like a safety vest. But what do I do when my "best friend" is also my entire routine? What do I do when my inspiration to wake up, to work, to struggle through this new country, is tied to a man I’m supposed to eventually "move on" from?</p>
            <p>I’m scared, Abhi. I’m scared that by staying "just friends," I am agreeing to a future where one day, I won't be the one cleaning up after your party.</p>
            <p>I can be your supporter. I can be your rock. I can be the person who knows your coffee order and your mother’s favorite cake by heart. But deep down, I don't know how to rewrite my story without you as the lead character.</p>
            <p>Thank you for being my constant in a world of chaos. Even if I don't know where we are going, I’m glad it was you who taught me how to walk through the mist.</p>
            <div style="text-align: right; color: #FF6B6B; font-weight: bold; font-size: 1.5rem; margin-top: 30px;">
                Always yours, in every way that matters,<br>
                Potti
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- SUB-PAGE: PRIVATE MOMENTS (SLIDESHOW) ---
    elif st.session_state.get('viewing_us_photos', False):
        if st.button("🔙 Back to Journey Vault", key="us_vault_back"): 
            st.session_state.viewing_us_photos = False; st.rerun()
        
        st.markdown("<h1 style='text-align:center;'>❤️ Our Private Moments</h1>", unsafe_allow_html=True)

        # 1. MOVED TO TOP: Reveal a Reason
        _, heart_c, _ = st.columns([1, 2, 1])
        with heart_c:
            if st.button("❤️ Reveal a Reason for this Memory", key="reason_action_top", use_container_width=True):
                reasons = [
                    "Because you crossed an ocean, and I followed.", 
                    "Because you know the exact brand of chocolates to bring me when I'm sick.",
                    "Because you taught me I don't need headphones to find peace.",
                    "Because you're the only routine I ever truly wanted to keep.",
                    "Because you are my geography—the map I use to navigate the world.",
                    "Because with you, I lived a life composed entirely of 'firsts'.",
                    "Because you make me feel like the absolute center of your universe.",
                    "Because you are the silent architect of my confidence."
                ]
                st.session_state.current_reason = random.choice(reasons); st.snow()
        
        if st.session_state.current_reason:
            st.markdown(f'<div style="background:rgba(255,255,255,0.1); backdrop-filter:blur(10px); border-radius:20px; padding:20px; text-align:center; margin-bottom:20px; border: 1px solid rgba(255,255,255,0.3);"><p style="font-size:1.3rem; font-style:italic;">"{st.session_state.current_reason}"</p></div>', unsafe_allow_html=True)

        # 2. Slideshow Navigation
        us_photos = [f"us_{i}.jpg" for i in range(1, 19)]
        curr_idx = st.session_state.photo_index
        prev_c, img_c, next_c = st.columns([1, 4, 1])
        with prev_c:
            st.write("##")
            if st.button("⬅️ Prev", key="p_us_btn"): st.session_state.photo_index = (curr_idx - 1) % 18; st.rerun()
        with img_c:
            img_b64 = get_image_base64(f"gallery/{us_photos[curr_idx]}")
            if img_b64:
                st.markdown(f'<div style="text-align:center; border:10px solid white; border-radius:20px; background:white; padding:15px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);"><img src="data:image/jpeg;base64,{img_b64}" style="max-width:100%; border-radius:10px;"><p style="color:#2c3e50; font-weight:bold; margin-top:10px;">Memory {curr_idx + 1} of 18</p></div>', unsafe_allow_html=True)
        with next_c:
            st.write("##")
            if st.button("➡️ Next", key="n_us_btn"): st.session_state.photo_index = (curr_idx + 1) % 18; st.rerun()

        # 3. ADDED: Full Collection Grid
        st.write("---")
        st.markdown("<h2 style='text-align:center;'>📸 The Full Collection</h2>", unsafe_allow_html=True)
        
        # Checking extensions for 18 photos to ensure they all load
        grid = st.columns(3)
        extensions = [".jpg", ".jpeg", ".png", ".JPG"]
        
        for i in range(1, 19):
            img_grid_b64 = None
            for ext in extensions:
                photo_name = f"us_{i}{ext}"
                img_grid_b64 = get_image_base64(f"gallery/{photo_name}")
                if img_grid_b64:
                    break
            
            with grid[(i-1) % 3]:
                if img_grid_b64:
                    st.markdown(f'''
                        <div class="photo-card" style="margin-bottom:20px;">
                            <img src="data:image/jpeg;base64,{img_grid_b64}" 
                                 style="width:100%; height:250px; object-fit:cover;">
                        </div>
                    ''', unsafe_allow_html=True)

                    
    # --- MAIN JOURNEY VAULT ---
    else:
        st.markdown("<h1 style='text-align:center;'>❤️ Our Journey Vault ❤️</h1>", unsafe_allow_html=True)
        phase_links = {
            "Phase I": "https://gemini.google.com/share/a836962563ae",
            "Phase II": "https://gemini.google.com/share/527cb5d2d1ab",
            "Phase III": "https://gemini.google.com/share/b82ddc6db85b",
            "Phase IV": "https://gemini.google.com/share/55186d27a858",
            "Phase V": "https://gemini.google.com/share/70f2963dcb79",
            "Phase VI": "https://gemini.google.com/share/6871d47d1f6a",
            "Phase VII": "https://gemini.google.com/share/9d8bec2afd20",
            "Phase VIII": "https://gemini.google.com/share/a847fa96defd"
        }
        phases = [ 
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
                card_html = f"""
                    <div style="background:rgba(255,255,255,0.95); border-radius:20px; overflow:hidden; border-top:10px solid {color}; text-align:center; color:#2c3e50; height: 350px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                        <img src="data:image/png;base64,{img_b64}" style="width:100%; height:200px; object-fit:cover;">
                        <div style="padding:15px;">
                            <h4 style="color:{color}; margin:0;">{p_id}</h4>
                            <h3 style="margin:5px 0; color:#2c3e50;">{title}</h3>
                """
                if p_id == "Final":
                    st.markdown(card_html + "</div></div>", unsafe_allow_html=True)
                    if st.button("💌 Open Letter", key="final_letter_btn", use_container_width=True):
                        st.session_state.viewing_letter = True; st.rerun()
                else:
                    link = phase_links.get(p_id, "#")
                    st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none;">{card_html}<p style="font-size:0.8rem; color:#666;">📖 Read Story</p></div></a>', unsafe_allow_html=True)
        st.write("---")
        _, center_btn, _ = st.columns([1, 2, 1])
        with center_btn:
            if st.button("🔓 UNLOCK THE US VAULT (PRIVATE GALLERY)", key="unlock_us_vault_btn", use_container_width=True):
                st.session_state.viewing_us_photos = True; st.balloons(); st.rerun()

    if st.button("🔙 Logout", key="global_logout_btn"):
        st.session_state.authenticated = False; st.session_state.page = "landing"; st.rerun()
