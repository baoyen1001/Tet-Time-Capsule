import streamlit as st
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import datetime, date
import time

# --- 1. CONFIGURATION ---
cloudinary.config( 
  cloud_name = "diirli2p5", 
  api_key = "734765651265494", 
  api_secret = "MhEUSTq3Vl_KwUT_sWSZt0VPiak",
  secure = True
)
FOLDER_NAME = "BaoYen_Memories_2026"

# --- 2. PAGE SETUP ---
st.set_page_config(
    page_title="BAO & YEN",
    page_icon=None, # Không dùng icon
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. DATA INITIALIZATION ---
if 'timeline' not in st.session_state:
    st.session_state.timeline = [
        {"date": date(2026, 1, 10), "title": "THE BEGINNING", "desc": "Official Relationship Start Date"},
        {"date": date(2026, 2, 14), "title": "FIRST VALENTINE", "desc": "Dinner at The Deck Saigon"},
    ]
if 'wishes' not in st.session_state:
    st.session_state.wishes = []
if 'love_start_date' not in st.session_state:
    st.session_state.love_start_date = date(2026, 1, 10)

# --- 4. PROFESSIONAL CSS (SWISS STYLE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Lato:wght@300;400;700&display=swap');

    /* GLOBAL RESET */
    .stApp {
        background-color: #ffffff;
        color: #1a1a1a;
    }
    
    h1, h2, h3 {
        font-family: 'Cinzel', serif;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #000;
    }
    
    p, div, span, button, input {
        font-family: 'Lato', sans-serif;
        font-weight: 300;
    }

    /* HEADER STYLE */
    .header-container {
        text-align: center;
        padding: 60px 0;
        border-bottom: 1px solid #eee;
        margin-bottom: 40px;
    }
    .main-title {
        font-size: 4rem;
        margin-bottom: 10px;
        letter-spacing: 5px;
    }
    .sub-title {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    .counter-box {
        margin-top: 20px;
        font-size: 1.2rem;
        font-weight: 700;
        border: 1px solid #000;
        display: inline-block;
        padding: 10px 30px;
    }

    /* TABS STYLE */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 40px;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Lato', sans-serif;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        background-color: transparent;
        border: none;
        color: #999;
        padding-bottom: 5px;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #000 !important;
        border-bottom: 2px solid #000;
    }

    /* CARD STYLE (MUSEUM) */
    .gallery-item {
        margin-bottom: 40px;
    }
    .gallery-img {
        width: 100%;
        display: block;
        filter: grayscale(100%); /* Ảnh đen trắng nghệ thuật */
        transition: all 0.5s ease;
    }
    .gallery-img:hover {
        filter: grayscale(0%); /* Di chuột vào hiện màu */
    }
    .gallery-info {
        margin-top: 15px;
        border-left: 1px solid #000;
        padding-left: 15px;
    }
    .gallery-date {
        font-size: 0.7rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .gallery-caption {
        font-size: 0.9rem;
        text-transform: uppercase;
        margin-top: 5px;
        font-weight: 400;
    }

    /* TIMELINE STYLE */
    .timeline-row {
        border-bottom: 1px solid #eee;
        padding: 30px 0;
        display: flex;
        align-items: center;
    }
    .timeline-date {
        width: 20%;
        font-family: 'Cinzel', serif;
        font-size: 1.5rem;
        color: #ccc;
    }
    .timeline-content {
        width: 80%;
    }

    /* INPUT & BUTTONS */
    div.stButton > button {
        background-color: #000;
        color: #fff;
        border-radius: 0;
        border: 1px solid #000;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 2px;
        padding: 12px 24px;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #fff;
        color: #000;
    }
    input, textarea, select {
        border-radius: 0 !important;
        border: 1px solid #ddd !important;
        font-family: 'Lato', sans-serif;
    }
    
    /* HIDE STREAMLIT UI */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 5. HELPER FUNCTIONS ---
def get_media():
    try:
        return cloudinary.api.resources(type="upload", prefix=FOLDER_NAME, context=True, max_results=100, direction="desc").get('resources', [])
    except:
        return []

def upload_media(file, caption, author):
    try:
        return cloudinary.uploader.upload(file, folder=FOLDER_NAME, context=f"caption={caption}|author={author}")
    except:
        return None

def get_days_together():
    delta = date.today() - st.session_state.love_start_date
    return delta.days

# --- 6. MAIN APP ---
def main():
    
    # --- HEADER ---
    days = get_days_together()
    st.markdown(f"""
    <div class="header-container">
        <div class="main-title">BAO & YEN</div>
        <div class="sub-title">ESTABLISHED 2026 • HO CHI MINH CITY</div>
        <div class="counter-box">{days} DAYS TOGETHER</div>
    </div>
    """, unsafe_allow_html=True)

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs(["GALLERY", "TIMELINE", "ARCHIVE"])

    # === TAB 1: GALLERY ===
    with tab1:
        # Upload Section (Minimalist)
        with st.expander("UPLOAD NEW ENTRY"):
            with st.form("upload_form"):
                c1, c2 = st.columns([1, 2])
                author = c1.selectbox("AUTHOR", ["BAO", "YEN"])
                caption = c2.text_input("CAPTION")
                file = st.file_uploader("FILE", type=['jpg','png','mp4'])
                if st.form_submit_button("PUBLISH"):
                    if file:
                        upload_media(file, caption, author)
                        st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)

        media = get_media()
        if not media:
            st.caption("NO DATA AVAILABLE.")
        
        # Grid Display
        cols = st.columns(3)
        for i, item in enumerate(media):
            ctx = item.get('context', {}).get('custom', {})
            url = item.get('secure_url')
            
            with cols[i % 3]:
                st.markdown('<div class="gallery-item">', unsafe_allow_html=True)
                
                if item.get('format') == 'mp4':
                    st.video(url)
                else:
                    # Ảnh có class gallery-img (đen trắng -> màu)
                    st.markdown(f'<img src="{url}" class="gallery-img">', unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="gallery-info">
                        <div class="gallery-date">{item.get('created_at')[:10]} / {ctx.get('author','').upper()}</div>
                        <div class="gallery-caption">{ctx.get('caption','').upper()}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # === TAB 2: TIMELINE ===
    with tab2:
        # Add Event
        with st.expander("ADD EVENT"):
            with st.form("add_timeline"):
                c1, c2 = st.columns([1,3])
                d = c1.date_input("DATE")
                t = c2.text_input("TITLE")
                desc = st.text_area("DESCRIPTION")
                if st.form_submit_button("RECORD EVENT"):
                    st.session_state.timeline.append({"date": d, "title": t, "desc": desc})
                    st.session_state.timeline.sort(key=lambda x: x['date'], reverse=True)
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display Timeline (List View)
        sorted_timeline = sorted(st.session_state.timeline, key=lambda x: x['date'], reverse=True)
        for event in sorted_timeline:
            st.markdown(f"""
            <div class="timeline-row">
                <div class="timeline-date">
                    {event['date'].strftime('%d')}<br>
                    <span style="font-size:1rem;">{event['date'].strftime('%b').upper()}</span>
                </div>
                <div class="timeline-content">
                    <h3 style="margin:0; font-size:1.2rem;">{event['title'].upper()}</h3>
                    <p style="color:#666; margin-top:5px;">{event['desc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # === TAB 3: ARCHIVE (Wishes) ===
    with tab3:
        # Write Letter
        with st.expander("COMPOSE LETTER"):
            with st.form("archive_form"):
                txt = st.text_area("CONTENT")
                unlock = st.date_input("UNLOCK DATE")
                if st.form_submit_button("STORE"):
                    st.session_state.wishes.append({"txt": txt, "date": date.today(), "unlock": unlock})
                    st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)

        # List Letters
        for i, w in enumerate(st.session_state.wishes):
            today = date.today()
            is_locked = today < w['unlock']
            
            status = "LOCKED" if is_locked else "OPEN"
            color = "#ccc" if is_locked else "#000"
            border = "1px solid #eee" if is_locked else "1px solid #000"
            
            st.markdown(f"""
            <div style="border: {border}; padding: 20px; margin-bottom: 20px;">
                <div style="display:flex; justify-content:space-between; border-bottom:1px solid #eee; padding-bottom:10px; margin-bottom:10px;">
                    <span style="font-weight:bold; letter-spacing:1px;">ID: {i+1:03}</span>
                    <span style="color:{color}; font-weight:bold;">STATUS: {status}</span>
                </div>
            """, unsafe_allow_html=True)
            
            if is_locked:
                st.markdown(f"""
                <div style="text-align:center; padding: 20px; color:#ccc; letter-spacing:2px;">
                    AVAILABLE ON {w['unlock'].strftime('%Y-%m-%d')}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="font-family:'Lato'; font-size:1.1rem; line-height:1.6;">
                    {w['txt']}
                </div>
                <div style="margin-top:20px; font-size:0.7rem; color:#888; text-transform:uppercase;">
                    CREATED: {w['date'].strftime('%Y-%m-%d')}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Delete button (Text only)
            if st.button("DELETE ENTRY", key=f"del_{i}"):
                st.session_state.wishes.pop(i)
                st.rerun()

if __name__ == "__main__":
    main()
