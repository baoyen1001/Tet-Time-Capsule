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
    page_title="BAO & YEN | The Journal",
    page_icon="🍂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. DATA INITIALIZATION (ENGLISH) ---
if 'timeline' not in st.session_state:
    st.session_state.timeline = [
        {"date": date(2026, 1, 10), "title": "THE BEGINNING", "desc": "The day our stars crossed paths."},
        {"date": date(2026, 2, 14), "title": "FIRST VALENTINE", "desc": "A romantic dinner under the starlight."},
    ]
if 'wishes' not in st.session_state:
    st.session_state.wishes = []
if 'love_start_date' not in st.session_state:
    st.session_state.love_start_date = date(2026, 1, 10)

# --- 4. HIGH-END EDITORIAL CSS ---
st.markdown("""
    <style>
    /* IMPORT FONTS:
       - Cormorant Garamond: Font có chân, sang trọng, HỖ TRỢ TIẾNG VIỆT TUYỆT ĐỐI.
       - Montserrat: Font hiện đại, sạch sẽ, dễ đọc.
    */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Montserrat:wght@300;400;500&display=swap');

    /* GLOBAL THEME */
    .stApp {
        background-color: #fdfcf0; /* Màu kem giấy cũ (Kinfolk style) */
        color: #2c2c2c;
    }

    /* TYPOGRAPHY */
    h1, h2, h3 {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #1a1a1a;
    }
    
    p, div, span, button, input, textarea {
        font-family: 'Montserrat', sans-serif;
        font-weight: 300;
        letter-spacing: 0.05em;
        line-height: 1.6;
    }

    /* HEADER SECTION */
    .editorial-header {
        text-align: center;
        padding: 80px 0 40px 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 50px;
    }
    .main-logo {
        font-size: 5rem;
        margin: 0;
        line-height: 1;
        font-style: italic; /* Chữ nghiêng nghệ thuật */
    }
    .sub-logo {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.3em;
        color: #888;
        margin-top: 10px;
    }
    .love-counter {
        margin-top: 30px;
        display: inline-block;
        border: 1px solid #c5a059; /* Viền vàng đồng */
        padding: 10px 40px;
        color: #c5a059;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.2rem;
        font-style: italic;
    }

    /* TABS STYLE */
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
        gap: 50px;
        background: transparent;
        padding-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        color: #aaa;
        border: none;
        background: transparent;
    }
    .stTabs [aria-selected="true"] {
        color: #1a1a1a !important;
        border-bottom: 1px solid #1a1a1a;
        background: transparent !important;
    }

    /* GALLERY GRID (MAGAZINE STYLE) */
    .gallery-frame {
        background: #fff;
        padding: 15px; /* Tạo khung trắng bo quanh ảnh */
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        margin-bottom: 40px;
        transition: transform 0.4s ease;
    }
    .gallery-frame:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.08);
    }
    .caption-text {
        margin-top: 15px;
        text-align: center;
        font-family: 'Cormorant Garamond', serif;
        font-style: italic;
        font-size: 1.2rem;
        color: #555;
    }
    .meta-text {
        text-align: center;
        font-size: 0.65rem;
        color: #bbb;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 5px;
    }

    /* TIMELINE (MINIMALIST) */
    .timeline-row {
        display: flex;
        padding: 30px 0;
        border-bottom: 1px solid #eee;
    }
    .t-date {
        width: 15%;
        font-family: 'Cormorant Garamond', serif;
        font-size: 2rem;
        color: #ddd;
        text-align: right;
        padding-right: 30px;
    }
    .t-content {
        width: 85%;
        border-left: 1px solid #1a1a1a;
        padding-left: 30px;
    }

    /* BUTTONS & INPUTS */
    div.stButton > button {
        background-color: transparent;
        color: #1a1a1a;
        border: 1px solid #1a1a1a;
        border-radius: 0;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.2em;
        padding: 12px 30px;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #1a1a1a;
        color: #fff;
    }
    
    input, textarea, select {
        background-color: #fff !important;
        border: 1px solid #eee !important;
        border-radius: 0 !important;
        color: #333 !important;
    }

    /* HIDE STREAMLIT ELEMENTS */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 5. FUNCTIONS ---
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

def get_days_count():
    delta = date.today() - st.session_state.love_start_date
    return delta.days

# --- 6. MAIN APP ---
def main():
    
    # --- HEADER ---
    days = get_days_count()
    st.markdown(f"""
    <div class="editorial-header">
        <h1 class="main-logo">Bao & Yen</h1>
        <div class="sub-logo">The Visual Journal • Est. 2026</div>
        <div class="love-counter">{days} Days of Love</div>
    </div>
    """, unsafe_allow_html=True)

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs(["MOMENTS", "JOURNEY", "CAPSULE"])

    # === TAB 1: MOMENTS (Gallery) ===
    with tab1:
        # Minimalist Upload Form
        with st.expander("PUBLISH NEW MOMENT"):
            with st.form("upload_form"):
                c1, c2 = st.columns([1, 2])
                author = c1.selectbox("AUTHOR", ["BAO", "YEN"])
                caption = c2.text_input("CAPTION (English or Vietnamese)")
                file = st.file_uploader("SELECT FILE", type=['jpg','png','mp4'])
                if st.form_submit_button("PUBLISH ENTRY"):
                    if file:
                        upload_media(file, caption, author)
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        media = get_media()
        if not media:
            st.caption("No entries found. Start your journal today.")
        
        # Magazine Grid Layout
        cols = st.columns(3)
        for i, item in enumerate(media):
            ctx = item.get('context', {}).get('custom', {})
            url = item.get('secure_url')
            
            with cols[i % 3]:
                st.markdown('<div class="gallery-frame">', unsafe_allow_html=True)
                
                if item.get('format') == 'mp4':
                    st.video(url)
                else:
                    st.image(url, use_column_width=True)
                
                st.markdown(f"""
                    <div class="caption-text">{ctx.get('caption','Untitled')}</div>
                    <div class="meta-text">{item.get('created_at')[:10]} • {ctx.get('author','UNKNOWN')}</div>
                </div>
                """, unsafe_allow_html=True)

    # === TAB 2: JOURNEY (Timeline) ===
    with tab2:
        # Add Event
        with st.expander("ADD MILESTONE"):
            with st.form("add_timeline"):
                c1, c2 = st.columns([1,3])
                d = c1.date_input("DATE")
                t = c2.text_input("TITLE")
                desc = st.text_area("DESCRIPTION")
                if st.form_submit_button("SAVE MILESTONE"):
                    st.session_state.timeline.append({"date": d, "title": t, "desc": desc})
                    st.session_state.timeline.sort(key=lambda x: x['date'], reverse=True)
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Timeline Display
        sorted_timeline = sorted(st.session_state.timeline, key=lambda x: x['date'], reverse=True)
        for event in sorted_timeline:
            st.markdown(f"""
            <div class="timeline-row">
                <div class="t-date">
                    {event['date'].strftime('%d')}<br>
                    <span style="font-size:1rem; color:#aaa;">{event['date'].strftime('%b').upper()}</span>
                </div>
                <div class="t-content">
                    <h3 style="margin:0; font-size:1.4rem; letter-spacing:0.05em;">{event['title'].upper()}</h3>
                    <p style="color:#666; margin-top:10px;">{event['desc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # === TAB 3: CAPSULE (Wishes) ===
    with tab3:
        # Letter Form
        col_form, col_display = st.columns([1, 2])
        
        with col_form:
            st.markdown("### WRITE A LETTER")
            with st.form("archive_form"):
                txt = st.text_area("MESSAGE", height=200)
                unlock = st.date_input("UNLOCK DATE")
                if st.form_submit_button("SEAL & STORE"):
                    st.session_state.wishes.append({"txt": txt, "date": date.today(), "unlock": unlock})
                    st.rerun()
        
        with col_display:
            st.markdown("### ARCHIVE")
            if not st.session_state.wishes:
                st.caption("Archive is empty.")
            
            for i, w in enumerate(st.session_state.wishes):
                today = date.today()
                is_locked = today < w['unlock']
                
                status_color = "#ccc" if is_locked else "#1a1a1a"
                border_style = "1px dashed #ccc" if is_locked else "1px solid #1a1a1a"
                
                st.markdown(f"""
                <div style="border: {border_style}; padding: 25px; margin-bottom: 20px; background: #fff;">
                    <div style="font-size:0.7rem; color:#aaa; letter-spacing:0.2em; margin-bottom:15px;">
                        ENTRY NO. {i+1:03}
                    </div>
                """, unsafe_allow_html=True)
                
                if is_locked:
                    days_left = (w['unlock'] - today).days
                    st.markdown(f"""
                    <div style="text-align:center; color:#ccc; font-family:'Cormorant Garamond'; font-size:1.5rem; font-style:italic;">
                        Locked until {w['unlock'].strftime('%B %d, %Y')}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="font-family:'Cormorant Garamond'; font-size:1.4rem; line-height:1.6; color:#1a1a1a;">
                        "{w['txt']}"
                    </div>
                    <div style="margin-top:20px; font-size:0.7rem; color:#ccc; letter-spacing:0.1em; text-transform:uppercase;">
                        Unlocked: {w['unlock'].strftime('%Y-%m-%d')}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                if st.button("REMOVE ENTRY", key=f"del_{i}"):
                    st.session_state.wishes.pop(i)
                    st.rerun()

if __name__ == "__main__":
    main()
